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

# Data Understanding
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
| 4   | `Location`            | object    | Lokasi pengguna dalam format.                       |
| 5   | `Age`                 | float64   | Usia pengguna.                                                               |
| 6   | `Book-Title`          | object    | Judul buku yang diberi rating.                                               |
| 7   | `Book-Author`         | object    | Nama penulis buku.                                                           |
| 8   | `Year-Of-Publication` | object    | Tahun terbit buku.                                                           |
| 9   | `Publisher`           | object    | Nama penerbit buku.                                                          |
| 10  | `Image-URL-S`         | object    | URL gambar ukuran kecil sampul buku.                                         |
| 11  | `Image-URL-M`         | object    | URL gambar ukuran sedang sampul buku.                                        |
| 12  | `Image-URL-L`         | object    | URL gambar ukuran besar sampul buku.                                         |


# Exploratory Data Analysis
#### 1. Distribusi Usia Pembaca
<p align="center">
  <img src="https://github.com/user-attachments/assets/3b333f89-51bd-4f61-949d-ab9115fb0a56" width="600"/>
</p>

> **Insight:**

> Berdasarkan histogram tersebut, dapat disimpulkan bahwa mayoritas pengguna dalam dataset ini adalah kalangan dewasa muda, dengan puncak distribusi usia terkonsentrasi secara signifikan antara 20 hingga 40 tahun. Grafik ini juga menunjukkan adanya right-skew (condong ke kanan), yang menandakan bahwa jumlah pengguna secara bertahap menurun seiring bertambahnya usia, meskipun masih ada basis pengguna yang cukup di usia paruh baya. Selain itu, terdapat indikasi kuat adanya data anomali atau outlier pada usia yang sangat rendah (mendekati 0) dan sangat tinggi (jauh di atas 100 tahun), yang mengindikasikan perlunya pembersihan data lebih lanjut sebelum analisis mendalam.

#### 2. Distribusi Buku yang Paling Banyak Dinilai

<p align="center">
  <img src="https://github.com/user-attachments/assets/f07e881f-b92d-4e5b-91c4-45d8bb819642" width="600"/>
</p>

> **Insight:**

> Popularitas buku dalam dataset diukur berdasarkan jumlah rating, bukan rata-rata skornya.
> Buku "Wild Animus" merupakan outlier yang sangat mencolok, dengan jumlah ulasan hampir dua kali lipat dibandingkan buku di peringkat kedua.
> Popularitas ekstrem "Wild Animus" kemungkinan besar tidak mencerminkan kualitas, melainkan dipengaruhi oleh faktor eksternal seperti kampanye pemasaran atau program distribusi buku gratis.
> Buku-buku lain dalam daftar Top 10 didominasi oleh fiksi populer dan bestseller, seperti "The Lovely Bones" dan "The Da Vinci Code".
> Hal ini menunjukkan bahwa selera mayoritas pengguna dalam dataset lebih condong ke buku fiksi komersial yang terkenal.

#### 3.Distribusi Penulis dengan Buku Paling Banyak Dirating
<p align="center">
  <img src="https://github.com/user-attachments/assets/ed581c6a-d68f-4306-9d9a-534d827240a4" width="600"/>
</p>

> **Insight:**

> Stephen King menempati posisi teratas sebagai penulis dengan karya terbanyak yang diulas oleh pengguna.
> Daftar 10 besar penulis didominasi oleh penulis fiksi komersial ternama seperti:
> - Nora Roberts
> - John Grisham
> - James Patterson

> Penulis-penulis tersebut dikenal sebagai 'powerhouse' dalam genre spesifik seperti:
> - Thriller
> - Misteri
> - Romance

> Preferensi mayoritas pembaca dalam dataset ini mengarah pada cerita-cerita penuh ketegangan (suspense) dan narasi romantis.
> Popularitas penulis dalam grafik ini tampak dibangun secara kumulatif dari banyaknya karya, bukan hanya dari satu buku yang sangat populer.


#### 4. Distribusi Jumlah Rating per Buku
<p align="center">
  <img src="https://github.com/user-attachments/assets/e5f2ae22-a00c-416a-8760-af9a62ed833b" width="600"/>
</p>

> **Insight**
> 1. Mayoritas interaksi dalam dataset adalah rating '0' (lebih dari 600.000 entri).
> 2. Rating '0' bukan berarti buruk, tetapi merupakan rating implisit, yang kemungkinan besar:
> Menandakan pengguna pernah berinteraksi dengan buku (misalnya, menambahkan ke rak), Namun tidak memberikan skor numerik secara eksplisit.
> 3. Jika hanya dilihat rating eksplisit (1–10):
>  - Terlihat bias ke arah skor positif, yaitu: Skor rendah (1–4) memiliki jumlah ulasan sangat sedikit,
> - Puncak jumlah rating terjadi pada skor 7 dan 8.

> 5. Temuan ini menunjukkan pentingnya:
> - Memisahkan rating implisit ('0') dan eksplisit (1–10) dalam analisis dan pemodelan,
> - Karena kedua jenis data ini mencerminkan perilaku pengguna yang berbeda.

## Data Quality Verifivation

#### 1. Mencari Missing Value
<p align="center">
  <img src="https://github.com/user-attachments/assets/1287746d-b38d-4ab4-8cd6-77e1ee904654" width="600"/>
</p>

> **Insight:**

> Terdapat missing value pada kolom `Age` sebanyak  277835 atau kurang dari 50% sehingga akan saya hapus data tersebut.

#### 2. Melihat Jumlah Pengarang, Penerbit, dan Tahun Terbit
<p align="center">
  <img src="https://github.com/user-attachments/assets/0e98dbf3-6084-4c8b-9e95-0674da51cbed" width="600"/>
</p>

> **insight:**

> Dapat dilihat bahwa pada data tahun masih belum seragam, ada yang menggunakan tanda petik dan ada yang tidak. Selain itu, terdapat data yang salah, yaitu *DK Publishing Inc* dan *Gallimard* yang seharusnya berada pada kolom Publisher (penerbit). Data ini akan dihapus pada bagian Data Preparation.

#### 3. Memeriksa Duplikasi Data
<p align="center">
  <img src="https://github.com/user-attachments/assets/39148691-7d1a-425c-8030-c9a35cb16ee3" width="600"/>
</p>

> **insight:**
> Tidak ditemukan duplikasi pada data

# Data Preparation 
## Data Cleaning
#### 1. Menghapus Nilai yang tertukar
<p align="center">
  <img src="https://github.com/user-attachments/assets/57b6a4e0-6d6d-418e-9b16-f56ff70b9bd9" width="600"/>
</p>

#### 2. Menghapus Kolom yang Tidak Dibutuhkan
<p align="center">
  <img src="https://github.com/user-attachments/assets/56614b5f-e244-4a42-9633-dfd2f0c779bb" width="600"/>
</p>

#### 3. Mengisi Nilai Kosong Pada Kolom Book-Author
<p align="center">
  <img src="https://github.com/user-attachments/assets/55723d74-bc21-4700-9af0-beacce209465" width="600"/>
</p>

#### 4. Mengubah Tipe Data
<p align="center">
  <img src="https://github.com/user-attachments/assets/e9057258-67a2-4024-bd64-03f97871009c" width="600"/>
</p>

#### 5. Deskripsi akhir Dataframe df_merged
<p align="center">
  <img src="https://github.com/user-attachments/assets/68dcab81-ba5a-4848-bfdf-96c0b60582bd" width="600"/>
</p>

# Modelling and Result
##### 1. Mmembuat dataframe baru dan mengambil kolom yang dibutuhkan
<p align="center">
  <img src="https://github.com/user-attachments/assets/25c8de18-0a9e-4683-9640-b02d4dc94fbf" width="600"/>
</p>

##### 2. Encoding 


















