import json
import os
from book import Book

class Library:
    def __init__(self, storage_file="library.json"):
        self.storage_file = storage_file
        self.books = []
        self.load_books()

    def add_book(self, book):
        self.books.append(book)
        self.save_books()
        print(f"'{book.title}' kütüphaneye eklendi.")

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