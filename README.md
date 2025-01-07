# Motor Shop API

Aplikasi REST API untuk manajemen toko motor dan aksesori menggunakan Flask dan MySQL.

## Deskripsi

Motor Shop API adalah sistem manajemen untuk toko motor yang memungkinkan pengguna untuk mengelola data motor dan aksesoris. API ini dibangun menggunakan Flask-RESTX dan MySQL sebagai database. Sistem ini menyediakan endpoint untuk operasi CRUD (Create, Read, Update, Delete) pada data motor dan aksesori.

## Fitur

- Manajemen data motor (CRUD)
  - Menambah data motor baru
  - Melihat semua data motor
  - Melihat detail motor berdasarkan ID
  - Mengupdate data motor
  - Menghapus data motor

- Manajemen data aksesori (CRUD)
  - Menambah data aksesoris baru
  - Melihat semua data aksesoris
  - Melihat detail aksesoris berdasarkan ID
  - Mengupdate data aksesoris
  - Menghapus data aksesoris

## Teknologi yang Digunakan

- Python 3.x
- Flask
- Flask-RESTX
- MySQL
- mysql-connector-python
- requests (untuk client)

## Instalasi

1. Clone repository ini
```bash
git clone [https://github.com/alfa219/motor_shop.git]
cd motor-shop-api
```

2. Buat virtual environment dan aktivasi
```bash
python -m venv venv
source venv/bin/activate  # untuk Linux/Mac
venv\Scripts\activate     # untuk Windows
```

3. Install dependensi
```bash
pip install -r requirements.txt
```

4. Siapkan database MySQL
- Buat database baru bernama `motor_shop`
- Buat tabel yang diperlukan menggunakan struktur berikut:

```sql
CREATE TABLE motors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    brand VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,
    engine_capacity INT NOT NULL,
    year_of_production INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE accessories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);
```

5. Konfigurasi database
- Buka file `app.py`
- Sesuaikan konfigurasi database:
```python
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "motor_shop"
}
```

## Penggunaan

1. Jalankan server API
```bash
python app.py
```
Server akan berjalan di `http://localhost:8000`

2. Jalankan client untuk mengakses API
```bash
python client.py
```

3. Akses dokumentasi API melalui Swagger UI:
```
http://localhost:8000
```

## Struktur API

### Endpoint Motor

- GET `/motors` - Mengambil semua data motor
- POST `/motors` - Menambah motor baru
- GET `/motors/{id}` - MendaMengambil patkan detail motor berdasarkan ID
- PUT `/motors/{id}` - Mengupdate data motor
- DELETE `/motors/{id}` - Menghapus data motor

### Endpoint Aksesori

- GET `/accessories` - MendaMengambil patkan semua data aksesoris
- POST `/accessories` - Menambah aksesori baru
- GET `/accessories/{id}` - MendaMengambil patkan detail aksesoris berdasarkan ID
- PUT `/accessories/{id}` - Mengupdate data aksesoris
- DELETE `/accessories/{id}` - Menghapus data aksesoris




