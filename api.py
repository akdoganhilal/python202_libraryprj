from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from library import Library, Book
from database import Database
import httpx

app = FastAPI()
db = Database()
db.create_table()
library = Library()

class BookSchema(BaseModel):
    title: str
    author: str
    isbn: str

class ISBNRequest(BaseModel):
    isbn: str

class BookUpdate(BaseModel):
    title: str
    author: str

@app.get("/books", response_model=list[BookSchema])
def list_all_books():
    """
    Kütüphanedeki tüm kitapların listesini döndürür.
    """
    book_data = []
    for book in library.books:
        book_data.append({"title": book.title, "author": book.author, "isbn": book.isbn})
    return book_data

@app.get("/books/{isbn}", response_model=BookSchema)
def get_single_book(isbn: str):
    """
    Belirtilen ISBN'e sahip tek bir kitabı bulur ve döndürür.
    """
    found_book = library.find_book(isbn)
    if not found_book:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı.")
    return found_book

@app.post("/books", response_model=BookSchema)
def add_new_book(request: ISBNRequest):
    isbn = request.isbn
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
        return new_book
    
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"Hata: ISBN numarası '{isbn}' ile kitap bulunamadı. (Hata Kodu: {exc.response.status_code})"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Beklenmedik bir hata oluştu: {e}"
        )

@app.put("/books/{isbn}", response_model=BookSchema)
def update_existing_book(isbn: str, updated_book: BookUpdate):
    found_book = library.find_book(isbn)
    if not found_book:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı.")
    
    library.update_book(isbn, updated_book.title, updated_book.author)
    
    updated_book_obj = library.find_book(isbn)
    return updated_book_obj

@app.delete("/books/{isbn}")
def remove_existing_book(isbn: str):
    book_to_remove = library.find_book(isbn)
    if not book_to_remove:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı.")
    
    library.remove_book(isbn)
    return {"message": f"Kitap '{isbn}' başarıyla silindi."}