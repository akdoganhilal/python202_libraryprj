import httpx
import json
from library import Library
from book import Book

def display_menu():
    print("\n--- Kütüphane Yönetim Sistemi ---")
    print("1. Kitap Ekle")
    print("2. Kitap Sil")
    print("3. Kitapları Listele")
    print("4. Kitap Ara")
    print("5. Çıkış")
    print("-----------------------------------")

def main():
    library = Library()

    while True:
        display_menu()
        choice = input("Lütfen bir seçenek girin: ")

        if choice == '1':
            isbn = input("Kitabın ISBN numarasını girin: ")
            
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
                library.add_book(new_book)
                
            except httpx.HTTPStatusError as exc:
                print(f"Hata: ISBN numarası '{isbn}' ile kitap bulunamadı. (Hata Kodu: {exc.response.status_code})")
            except httpx.RequestError as exc:
                print(f"İstek Hatası: İnternet bağlantısı veya API'de sorun olabilir. Detay: {exc}")
            except json.JSONDecodeError:
                print("Hata: API'den geçersiz bir JSON yanıtı alındı.")
            except Exception as e:
                print(f"Beklenmedik bir hata oluştu: {e}")
        
        elif choice == '2':
            isbn = input("Silmek istediğiniz kitabın ISBN numarasını girin: ")
            library.remove_book(isbn)
        
        elif choice == '3':
            library.list_books()
        
        elif choice == '4':
            isbn = input("Aramak istediğiniz kitabın ISBN numarasını girin: ")
            found_book = library.find_book(isbn)
            if found_book:
                print(f"Kitap bulundu: {found_book}")
            else:
                print(f"ISBN numarası '{isbn}' olan kitap bulunamadı.")
        
        elif choice == '5':
            print("Uygulamadan çıkılıyor. Güle güle!")
            break
        
        else:
            print("Geçersiz seçenek. Lütfen 1 ile 5 arasında bir sayı girin.")

if __name__ == "__main__":
    main()