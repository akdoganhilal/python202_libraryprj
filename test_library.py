import pytest
from library import Library
from book import Book
import os

@pytest.fixture(autouse=True)
def cleanup():
    yield
    if os.path.exists("test_library.json"):
        os.remove("test_library.json")

@pytest.fixture
def test_library():
    return Library(storage_file="test_library.json")

# AŞAMA 1 ve 2 TESTİ: OOP ve Harici API entegrasyonu
# Bu test, Library sınıfının temel fonksiyonlarını (ekleme, silme, arama) ve harici API'den veri çekme özelliğini doğrular.
def test_add_and_remove_book(test_library):
    assert len(test_library.books) == 0
    
    test_isbn = "9780451526342" 
    test_library.add_book(test_isbn)
    assert len(test_library.books) == 1
    
    found_book = test_library.find_book(test_isbn)
    assert found_book is not None
    assert found_book.title == "Animal Farm"
    
    test_library.remove_book(test_isbn)
    assert len(test_library.books) == 0
    assert test_library.find_book(test_isbn) is None