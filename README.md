# Python Kütüphane Yönetim Sistemi
Bu proje, Python'da Nesne Yönelimli Programlama (OOP), harici API kullanımı ve FastAPI ile kendi web servisini oluşturma konularını birleştiren kapsamlı bir kütüphane yönetim uygulamasıdır. Proje, temel bir terminal uygulamasından başlayarak, web arayüzüne ve en sonunda bir Docker konteynerine dönüştürülmüştür.

### Proje Özellikleri
**OOP**: *Book* ve *Library* sınıfları kullanılarak kod, modüler ve yönetilebilir bir yapıda tasarlanmıştır.
**Harici API Entegrasyonu**: Open Library API'si üzerinden ISBN numarasıyla kitap bilgileri otomatik olarak çekilir.
**Veritabanı**: Veriler, kalıcı olarak bir SQLite veritabanında saklanır.
**RESTful API**: FastAPI ile kitapları listeleme, ekleme, silme ve güncelleme işlemleri için RESTful endpoint'ler oluşturulmuştur.
**Web Arayüzü**: Kendi API'mizi kullanan, HTML, CSS ve JavaScript ile geliştirilmiş basit bir yönetim paneli mevcuttur.
**Docker Desteği**: Proje, bir Docker konteyneri içinde çalıştırılabilir.

---

## Kurulum ve Başlangıç
Bu projeyi çalıştırmak için öncelikle bilgisayarınızda *Python 3.9+* ve *Docker* yüklü olmalıdır.

### 1 - Depoyu Klonlama
Projeyi bilgisayarınıza indirmek için aşağıdaki komutu kullanabilirsiniz:

git clone https://github.com/akdoganhilal/python202_libraryprj.git
cd python202_libraryprj

### 2 - Bağımlılıkları Kurma
Projenin çalışması için gerekli Python kütüphanelerini kurun:
pip install -r requirements.txt

### 3 - Docker ile Çalıştırma (Önerilen)
Docker, tüm bağımlılıkları otomatik olarak kurar ve sanal ortam oluşturmanıza gerek kalmaz. Projeyi en kolay çalıştırma yöntemidir.

#### 3.1 - Docker Görüntüsünü Oluşturma:
Proje klasörünün ana dizinindeyken aşağıdaki komutu çalıştırın:
docker build -t kutuphane-uygulamasi .

#### 3.2 - Docker Konteynerini Çalıştırma:
Görüntü oluşturulduktan sonra uygulamayı başlatın:
docker run -p 8000:8000 kutuphane-uygulamasi

API'niz artık *http://localhost:8000* adresinde çalışmaktadır.

***

## Kullanım
### Terminal Uygulaması
Projenin konsol tabanlı versiyonunu başlatmak için (API servisi çalışmıyorken):
python main.py

### API Servisi
Web servisini başlatmak ve API üzerinden erişim sağlamak için (Docker kullanmıyorsanız):
uvicorn api:app --reload

Bu komutu çalıştırdıktan sonra API'nin dokümantasyonuna *http://localhost:8000/docs* adresinden erişebilirsiniz.

### Web Arayüzü (Frontend)
API servisi çalıştıktan sonra, projenin ana dizinindeki *frontend/index.html* dosyasını tarayıcınızda açın. Bu sayfa üzerinden kitap ekleme, silme ve güncelleme işlemlerini görsel olarak gerçekleştirebilirsiniz.

***

## API Endpoint'leri
**GET /books**: Kütüphanedeki tüm kitapların listesini döndürür.
**GET /books/{isbn}**: Belirtilen ISBN'e sahip kitabı getirir.
**POST /books**: Yeni bir kitabı API'den çekerek ekler.
*Gövde Örneği*: *{"isbn": "9780451524935"}*
**PUT /books/{isbn}**: Bir kitabın başlık ve/veya yazar bilgilerini günceller.
*Gövde Örneği*: *{"title": "Yeni Başlık"}*
**DELETE /books/{isbn}**: Belirtilen ISBN'e sahip kitabı siler.

***

## Testler
Projenin güvenilirliğini sağlamak için *pytest* ile birim ve API testleri yazılmıştır. Terminalde aşağıdaki komutu çalıştırarak tüm testleri çalıştırabilirsiniz:

pytest