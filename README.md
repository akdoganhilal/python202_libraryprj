# Python Kütüphane Yönetim Sistemi
Bu proje, Nesne Yönelimli Programlama (OOP), harici API kullanımı ve FastAPI ile kendi web servisini oluşturma konularını birleştiren bir kütüphane yönetim uygulamasıdır. Kullanıcılar, ISBN numarası üzerinden kitap ekleyebilir, silebilir ve listeleyebilirler. Veriler, kalıcı olarak bir JSON dosyasında saklanmaktadır.

---

## Kurulum
### Depoyu Klonlama
Projeyi bilgisayarınıza indirmek için aşağıdaki komutu kullanabilirsiniz:
git clone https://github.com/akdoganhilal/python202_libraryprj.git

### Bağımlılıkları Kurma
Projenin çalışması için gerekli Python kütüphanelerini kurun:
pip install -r requirements.txt

***

## Kullanım
### Terminal Uygulaması
Konsol tabanlı menüyü başlatmak için:
python main.py

### API Servisi
Web servisini başlatmak ve API üzerinden erişim sağlamak için:
uvicorn api:app --reload

***

## API Dokümantasyonu
### GET /books
Kütüphanedeki tüm kitapların listesini JSON formatında döndürür.
[
  {"title": "Nineteen Eighty-Four", "author": "George Orwell", "isbn": "9780451524935"}
]

### POST /books
Verilen ISBN numarasına göre bir kitabı Open Library API'den çekerek kütüphaneye ekler.
{
  "isbn": "9780451524935"
}

### DELETE /books/{isbn}
URL'de belirtilen ISBN numarasına sahip kitabı kütüphaneden siler.