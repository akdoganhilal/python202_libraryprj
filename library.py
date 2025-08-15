import json
import os
from book import Book
import httpx

class Library:
    def __init__(self, storage_file="library.json"):
        self.storage_file = storage_file
        self.books = []
        self.load_books()

    def add_book(self, isbn):
        api_url = f"https://openlibrary.org/isbn/{isbn}.json"
        
        try:
            response = httpx.get(api_url, follow_redirects=True)
            response.raise_for_status()
            book_data = response.json()
            
            title = book_data.get("title", "Başlık bilgisi bulunamadı")
            author = "Yazar bilgisi bulunamadı"
            
            authors_data = book_data.get("authors")
            if authors_data and isinstance(authors_data, list) and authors_data[0].get("key"):
                first_author_key = authors_data[0].get("key")
                author_api_url = f"https://openlibrary.org{first_author_key}.json"
                
                try:
                    author_response = httpx.get(author_api_url)
                    author_response.raise_for_status()
                    author_data = author_response.json()
                    author = author_data.get("name", "Yazar bilgisi bulunamadı")
                except (httpx.HTTPStatusError, httpx.RequestError):
                    pass
            
            new_book = Book(title, author, isbn)
            self.books.append(new_book)
            self.save_books()
            print(f"'{title}' by {author} kütüphaneye eklendi.")

        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                print(f"Hata: ISBN numarası '{isbn}' ile kitap bulunamadı. (Hata Kodu: 404)")
            else:
                print(f"HTTP Hatası: {exc.response.status_code}")
        except httpx.RequestError as exc:
            print(f"İstek Hatası: İnternet bağlantısı veya Open Library API'sinde sorun olabilir. Detay: {exc}")
        except json.JSONDecodeError:
            print("Hata: API'den geçersiz bir JSON yanıtı alındı.")
        except Exception as e:
            print(f"Beklenmedik bir hata oluştu. Detay: {e}")

    def remove_book(self, isbn):
        book_to_remove = self.find_book(isbn)
        if book_to_remove:
            self.books.remove(book_to_remove)
            self.save_books()
            print(f"'{book_to_remove.title}' kütüphaneden silindi.")
        else:
            print(f"ISBN numarası '{isbn}' olan kitap bulunamadı.")

    def list_books(self):
        if not self.books:
            print("Kütüphanede henüz kitap bulunmuyor.")
            return

        print("\n--- Kütüphanedeki Kitaplar ---")
        for book in self.books:
            print(book)
        print("-----------------------------\n")

    def find_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def load_books(self):
        if os.path.exists(self.storage_file) and os.path.getsize(self.storage_file) > 0:
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.books = [Book(item['title'], item['author'], item['isbn']) for item in data]
        else:
            self.books = []
            self.save_books()

    def save_books(self):
        data = [{'title': b.title, 'author': b.author, 'isbn': b.isbn} for b in self.books]
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)