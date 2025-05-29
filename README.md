# Laporan Proyek Machine Learning - Ferry Pebriansyah
# Sistem Rekomendasi Buku

- **Nama:** Ferry Pebriansyah
- **Email:** ferryfeb10@gmail.com
- **ID Dicoding:** ferrypebriansyah

# Project Overview

Dalam era digital, pengguna menghadapi tantangan information overload dalam memilih bacaan dari jutaan judul buku yang tersedia secara online [1]. Sistem rekomendasi buku berbasis Collaborative Filtering efektif membantu mengatasi masalah ini dengan mempelajari pola rating antar pengguna untuk memberikan rekomendasi yang relevan tanpa memerlukan informasi lengkap tentang buku [2][3].
Proyek ini membangun sistem rekomendasi berbasis Collaborative Filtering menggunakan embedding neural network dengan data rating eksplisit sebagai input utama, sejalan dengan pendekatan yang telah dilakukan di berbagai studi lokal [1][4]. Pendekatan ini penting karena banyak platform digital hanya memiliki data interaksi pengguna tanpa metadata lengkap [2].
Beberapa penelitian di Indonesia menunjukkan keberhasilan Collaborative Filtering dalam sistem rekomendasi buku, seperti implementasi algoritma K-Nearest Neighbors dengan evaluasi menggunakan MAE dan RMSE [1], serta penerapan pada perpustakaan daerah dengan fokus pada akurasi prediksi [2]. Penggunaan metode ini juga terbukti efektif untuk toko buku online dalam meningkatkan relevansi rekomendasi [3][4].
Dengan mengoptimalkan data interaksi pengguna, proyek ini diharapkan dapat memberikan rekomendasi yang personal dan akurat serta mendukung perkembangan literasi digital melalui teknologi personalisasi [1][4].

# Business Understanding
## Problem Statements
Rumusan masalah yang dijawab dalam proyek ini adalah:
1. Apa saja buku yang paling banyak mendapatkan rating dari pengguna, dan bagaimana karakteristiknya?
2. Bagaimana cara membangun sebuah sistem yang mampu memberikan rekomendasi buku yang relevan dan personal kepada pengguna, dengan hanya memanfaatkan riwayat rating eksplisit mereka?

## Goals
Berdasarkan problem statements di atas, tujuan yang berhasil dicapai pada proyek ini adalah:
1. Mengidentifikasi buku, penulis, dan karakteristik lainnya yang paling sering mendapatkan rating dari pengguna, berdasarkan analisis data rating eksplisit.
2. Membangun sebuah model sistem rekomendasi fungsional yang memberikan saran bacaan baru yang dipersonalisasi untuk setiap pengguna.

## Solution Approach
Untuk mencapai goals tersebut, pendekatan solusi yang telah diimplementasikan adalah:
1. Data Preparation dan Filtering:
Melakukan pembersihan dan filtering data dengan menghapus anomali dan memastikan hanya data rating eksplisit (skor 1–10) yang digunakan. Data diubah menjadi format pasangan (user_id, book_id, rating) yang sesuai untuk pemodelan embedding.
2. Implementasi Model Rekomendasi:
Membangun model Collaborative Filtering berbasis embedding neural network yang memetakan pengguna dan buku ke dalam ruang fitur berdimensi rendah. Model dilatih menggunakan loss function seperti Mean Squared Error (MSE) untuk meminimalkan perbedaan antara rating prediksi dan aktual.
3. Evaluasi Model:
Melakukan evaluasi menggunakan metrik Root Mean Squared Error (RMSE) untuk mengukur akurasi prediksi rating, serta Precision@K dan Recall@K untuk menilai relevansi rekomendasi yang diberikan kepada pengguna.
4. Output Rekomendasi:
Model menghasilkan daftar rekomendasi buku yang diprediksi paling sesuai dengan preferensi masing-masing pengguna, berdasarkan pola rating yang dipelajari tanpa memerlukan metadata buku.

## Data Understanding
Data yang digunakan untuk membuat sistem rekomendasi buku diambil dari platform open source Kaggle dan dipublikasikan oleh arashnic, [Book Recommendation Dataset](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset)
Dataset ini terdiri dari 3 tabel yaitu:
1. Books.csv (8 kolom dan 271360 data)
2. Users.csv (3 kolom dan  278859 data)
3. Ratings.csv (3 kolom dan 1149780 data)

ketiga tabel tersebut memiliki relasi antar table yang pada akhirnya saya lakukan *merged table*. Penjelasan setiap varible:
| No. | Kolom                 | Tipe Data | Deskripsi                                                                    |
| --- | --------------------- | --------- | ---------------------------------------------------------------------------- |
| 1   | `User-ID`             | int64     | ID unik pengguna yang memberikan rating buku.                                |
| 2   | `ISBN`                | object    | ISBN (International Standard Book Number) sebagai ID unik untuk setiap buku. |
| 3   | `Book-Rating`         | int64     | Nilai rating yang diberikan pengguna terhadap buku (biasanya 0–10).          |
| 4   | `Location`            | object    | Lokasi pengguna dalam format .                       |
| 5   | `Age`                 | float64   | Usia pengguna (ada missing values).                                          |
| 6   | `Book-Title`          | object    | Judul buku yang diberi rating.                                               |
| 7   | `Book-Author`         | object    | Nama penulis buku (ada nilai kosong).                                        |
| 8   | `Year-Of-Publication` | object    | Tahun terbit buku. Awalnya bertipe object karena terdapat nilai non-numerik. |
| 9   | `Publisher`           | object    | Nama penerbit buku (ada nilai kosong).                                       |
| 10  | `Image-URL-S`         | object    | URL gambar ukuran kecil sampul buku.                                         |
| 11  | `Image-URL-M`         | object    | URL gambar ukuran sedang sampul buku.                                        |
| 12  | `Image-URL-L`         | object    | URL gambar ukuran besar sampul buku (ada nilai kosong).                      |







