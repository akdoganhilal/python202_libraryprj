import sqlite3
from book import Book
from database import Database 

class Library:
    def __init__(self):
        self.db = Database()
        self.books = self.load_books()

    def add_book(self, book):
        try:
            self.db.connect()
            self.db.cursor.execute("INSERT INTO books (isbn, title, author) VALUES (?, ?, ?)",
                                   (book.isbn, book.title, book.author))
            self.db.conn.commit()
            print(f"'{book.title}' kütüphaneye eklendi.")
        except sqlite3.IntegrityError:
            print(f"Hata: '{book.title}' (ISBN: {book.isbn}) zaten kütüphanede mevcut.")
        finally:
            self.db.close()
        
        self.books = self.load_books()

    def remove_book(self, isbn):
        self.db.connect()
        self.db.cursor.execute("DELETE FROM books WHERE isbn = ?", (isbn,))
        self.db.conn.commit()
        self.db.close()
        print(f"ISBN numarası '{isbn}' olan kitap silindi.")
        
        self.books = self.load_books()

    def list_books(self):
        self.books = self.load_books()
        if not self.books:
            print("Kütüphanede henüz kitap bulunmuyor.")
            return

        print("\n--- Kütüphanedeki Kitaplar ---")
        for book in self.books:
            print(book)
        print("-----------------------------\n")

    def find_book(self, isbn):
        self.db.connect()
        self.db.cursor.execute("SELECT title, author, isbn FROM books WHERE isbn = ?", (isbn,))
        row = self.db.cursor.fetchone()
        self.db.close()
        
        if row:
            return Book(row[0], row[1], row[2])
        return None

    def load_books(self):
        self.db.connect()
        self.db.cursor.execute("SELECT title, author, isbn FROM books")
        rows = self.db.cursor.fetchall()
        self.db.close()
        
        return [Book(row[0], row[1], row[2]) for row in rows]
    
    def update_book(self, isbn, title, author):
        self.db.connect()
        self.db.cursor.execute(
            "UPDATE books SET title = ?, author = ? WHERE isbn = ?",
            (title, author, isbn)
        )
        self.db.conn.commit()
        self.db.close()
        self.books = self.load_books()
        print(f"ISBN numarası '{isbn}' olan kitap güncellendi.")