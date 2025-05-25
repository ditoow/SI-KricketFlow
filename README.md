# 🦗 SI-KricketFlow

Sistem Informasi KricketFlow adalah aplikasi berbasis web untuk mengelola data peternakan jangkrik, termasuk pencatatan keuangan dan laporan akuntansi.

## Langkah-langkah Menjalankan Aplikasi

### 1. Instalasi Python

1. Download Python dari [website resmi Python](https://www.python.org/downloads/)
   - Pastikan untuk memilih Python versi 3.8 atau lebih baru
   - Pada Windows, centang opsi "Add Python to PATH" saat instalasi

2. Verifikasi instalasi Python dengan membuka Command Prompt atau Terminal:
   ```
   python --version
   ```
   atau
   ```
   python3 --version
   ```

### 2. Mengunduh Proyek

1. Unduh proyek SI-KricketFlow dari repository
2. Ekstrak file zip ke lokasi yang diinginkan di komputer Anda
3. Buka Command Prompt atau Terminal dan navigasi ke direktori proyek:
   ```
   cd path/to/SI-KricketFlow
   ```

### 3. Membuat Virtual Environment (Opsional tapi Direkomendasikan)

1. Buat virtual environment:
   ```
   python -m venv venv
   ```

2. Aktifkan virtual environment:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

### 4. Instalasi Dependencies

1. Pastikan Anda berada di direktori proyek dengan file `requirements.txt`
2. Install semua dependencies yang dibutuhkan:
   ```
   pip install -r requirements.txt
   ```

Summary : 
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

### 5. Setup Database

1. Jalankan script setup database untuk membuat struktur direktori yang dibutuhkan:
   - Windows:
     ```
     mkdir -p database
     ```
   - macOS/Linux:
     ```
     bash setup_database.sh
     ```

### 6. Menjalankan Aplikasi

1. Jalankan aplikasi dengan perintah:
   ```
   streamlit run App.py
   ```

2. Aplikasi akan terbuka secara otomatis di browser default Anda
   - Jika tidak, buka browser dan akses URL: http://localhost:8501

### 7. Login ke Aplikasi

1. Gunakan kredensial default untuk login pertama kali:
   - Username: `admin`
   - Password: `admiw`

### Struktur Direktori

```
SI-KricketFlow/
├── App.py                      # File utama aplikasi
├── assets                      # Aset gambar dan media
│   └── jangkrik.png
├── database                    # Direktori penyimpanan data
│   ├── bukubesar/              # Data buku besar
│   ├── jurnal_umum.csv         # File data jurnal
│   └── users.json              # Data pengguna
├── function                    # Modul fungsionalitas aplikasi
│   ├── auth.py                 # Autentikasi
│   ├── buku_besar.py           # Fungsi buku besar
│   ├── dashboard.py            # Fungsi dashboard
│   └── ...                     # Modul lainnya
├── setup_database.sh           # Script untuk setup database
└── requirements.txt            # Daftar dependencies
```

