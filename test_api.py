from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

# AŞAMA 3 TESTİ: API Endpoint'lerinin doğrulanması
# Bu test, GET /books endpoint'inin doğru çalıştığını kontrol eder.
def test_get_all_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# AŞAMA 3 TESTİ: API'ye POST ve DELETE işlemleri
# Bu test, kitap ekleme ve silme endpoint'lerinin doğru yanıt verdiğini kontrol eder.
def test_add_and_delete_book():
    test_isbn = "9780451526342"
    expected_title = "Animal Farm"
    
    add_response = client.post("/books", json={"isbn": test_isbn})
    assert add_response.status_code == 200
    assert add_response.json()["title"] == expected_title
    
    delete_response = client.delete(f"/books/{test_isbn}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Kitap '{test_isbn}' başarıyla silindi."