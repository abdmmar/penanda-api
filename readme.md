# Flask Tutorial

## Purpose
Proyek sederhana ini bertujuan untuk mempelajari cara membangun sebuah REST API menggunakan Flask, mengkonfigurasinya, menyusun proyek, menguji, dan mendeploy dengan Docker.

# Requirements
- Python 3.9.5
- Pipenv
- MySQL
- Docker
- docker-compose

## Setup
### docker-compose for Production(?)
1. Di folder `penanda-api` jalankan `docker-compose -f docker-compose.prod.yml up -d --build` untuk menjalankan container server menggunakan `waitress` dan juga database MySQL di port 3306

### docker-compose Development
1. Di folder `penanda-api` jalankan `docker-compose up --d --build` untuk menjalankan container server dan juga database MySQL di port 3307
2. Setelah container berjalan, maka API server pun dapat diakses di `localhost:5000`

### Lokal
1. Setalah container berhasil dijalankan, selanjutnya, API server bisa dijalankan secara terpisah jika ingin melakukan perubahan secara langsung tanpa perlu build ulang container dan juga karena database sudah dijalankan
2. Untuk menjalankan API Server, masuk ke dalam folder `/flask` dengan perintah `cd penanda-api/flask`
3. Jalankan `pipenv install` untuk memasang dependencies.
4. Jalankan `pipenv shell` untuk mengaktifkan lingkungan pengembangan. Ini harus diaktifkan sebelum setiap proses pengembangan.
5. Atur environment variable, tambahkan environment variable sesuai dengan CLI yang digunakan:
   - Powershell: `$env:FLASK_APP = app` and `$env:FLASK_ENV = development`
   - CMD: `set FLASK_APP = app` and `set FLASK_ENV = development`
   - Bash: `export FLASK_APP = "app"` and `export FLASK_ENV = "development"`
6. `flask run -p 5550` untuk menjalankan API server di port 5550
7. Akses `localhost:5550` di peramban, Postman, ataupun Insomnia untuk melihat bahwa API server sudah berhasil dijalankan

#### Catatan
- Untuk mengatur environment variable MySQL, bisa diubah di file `Dockerfile` dan `Dockerfile.prod`
- Untuk mengatur SECRET_KEY yang akan digunakan untuk autentikasi JWT, bisa diubah di `flask/.env`

## Dependencies
1. `Flask` framework untuk mendukung dalam pengembangan REST API ini
2. `flask-jwt-extended` untuk memudahkan dalam mengatur JSON Web Token (JWT)
3. `metadata-parser` untuk mengekstrak metadata dari sebuah pranala

## TODO
1. [ ] Bangun lama penanda menggunakan Next.js
2. [ ] Jalankan server menggunakan nginx
3. [ ] Menambahkan unit test dengan `pytest` dan `coverage`

## Articles
1. [A Short But Complete Guide To Python Flask App Development](https://medium.com/analytics-vidhya/a-short-but-complete-guide-to-python-flask-app-development-9b493f960bd1)
2. [Docker layer caching-friendly workflow with pipenv](https://github.com/pypa/pipenv/issues/3285)
3. [Building a Flask app with Docker](https://pythonise.com/series/learning-flask/building-a-flask-app-with-docker-compose)