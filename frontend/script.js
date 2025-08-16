document.addEventListener('DOMContentLoaded', () => {
    const addBookBtn = document.getElementById('addBookBtn');
    const addIsbnInput = document.getElementById('addIsbnInput');
    const updateBookBtn = document.getElementById('updateBookBtn');
    const deleteBookBtn = document.getElementById('deleteBookBtn');
    const manageIsbnInput = document.getElementById('manageIsbnInput');
    const updateTitleInput = document.getElementById('updateTitleInput');
    const updateAuthorInput = document.getElementById('updateAuthorInput');
    const listBooksBtn = document.getElementById('listBooksBtn');
    const bookList = document.getElementById('bookList');
    const API_URL = 'http://127.0.0.1:8000';

    async function fetchBooks() {
        try {
            const response = await fetch(`${API_URL}/books`, {
                mode: 'cors'
            });
            if (!response.ok) {
                throw new Error(`HTTP Hata! Durum: ${response.status}`);
            }
            const books = await response.json();
            
            bookList.innerHTML = ''; 
            if (books.length === 0) {
                bookList.innerHTML = '<p>Kütüphanede henüz kitap bulunmuyor.</p>';
            } else {
                books.forEach(book => {
                    const bookItem = document.createElement('div');
                    bookItem.className = 'book-item';
                    bookItem.innerHTML = `<strong>${book.title}</strong> by ${book.author} (ISBN: ${book.isbn})`;
                    bookList.appendChild(bookItem);
                });
            }
        } catch (error) {
            console.error('Kitaplar yüklenirken bir hata oluştu:', error);
            bookList.innerHTML = '<p>Kitaplar yüklenemedi. Lütfen sunucunun çalıştığından emin olun.</p>';
        }
    }

    addBookBtn.addEventListener('click', async () => {
        const isbn = addIsbnInput.value.trim();
        if (!isbn) return alert('Lütfen bir ISBN numarası girin.');

        try {
            const response = await fetch(`${API_URL}/books`, {
                method: 'POST',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ isbn: isbn })
            });
            const result = await response.json();
            if (!response.ok) {
                alert(result.detail || 'API hatası: Kitap eklenemedi.');
                console.error('API hatası:', result);
            } else {
                alert(`${result.title} başarıyla eklendi.`);
                fetchBooks();
            }
        } catch (error) {
            alert('Kitap eklenirken bir ağ hatası oluştu.');
            console.error(error);
        }
    });

    updateBookBtn.addEventListener('click', async () => {
        const isbn = manageIsbnInput.value.trim();
        const title = updateTitleInput.value.trim();
        const author = updateAuthorInput.value.trim();

        if (!isbn) return alert('Lütfen bir ISBN numarası girin.');
        if (!title && !author) return alert('Lütfen en az bir alanı (Başlık veya Yazar) doldurun.');

        try {
            const updateData = {};
            if (title) updateData.title = title;
            if (author) updateData.author = author;

            const response = await fetch(`${API_URL}/books/${isbn}`, {
                method: 'PUT',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(updateData)
            });

            const result = await response.json();
            if (!response.ok) {
                alert(result.detail || 'API hatası: Kitap güncellenemedi.');
                console.error('API hatası:', result);
            } else {
                alert(`${result.title} başarıyla güncellendi.`);
                fetchBooks();
            }
        } catch (error) {
            alert('Kitap güncellenirken bir ağ hatası oluştu.');
            console.error(error);
        }
    });

    deleteBookBtn.addEventListener('click', async () => {
        const isbn = manageIsbnInput.value.trim();
        if (!isbn) return alert('Lütfen bir ISBN numarası girin.');

        if (!confirm('Bu kitabı silmek istediğinizden emin misiniz?')) {
            return;
        }

        try {
            const response = await fetch(`${API_URL}/books/${isbn}`, {
                method: 'DELETE',
                mode: 'cors'
            });
            const result = await response.json();
            if (!response.ok) {
                alert(result.detail || result.message || 'API hatası: Kitap silinemedi.');
                console.error('API hatası:', result);
            } else {
                alert(result.message || 'Kitap başarıyla silindi.');
                fetchBooks();
            }
        } catch (error) {
            alert('Kitap silinirken bir ağ hatası oluştu.');
            console.error(error);
        }
    });

    listBooksBtn.addEventListener('click', fetchBooks);
    fetchBooks();
});
