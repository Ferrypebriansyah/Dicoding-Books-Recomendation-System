# -*- coding: utf-8 -*-
"""Ferry_Pebriansyah_Submission2_MLT_SR_v2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1bTXVaMrxGuRRbUa9h4561rHSbdlVLCuN

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

Tahap ini merupakan proses analisis data yang bertujuan untuk memperoleh pemahaman yang menyeluruh mengenai dataset sebelum melanjutkan ke tahap analisis lebih lanjut.

## 1. Mengimport Library

Pada bagian ini kita mengimport seluruh library yang diperlukan untuk menganalisis
"""

!pip install kaggle

!pip install keras

import os
import shutil
import zipfile
import textwrap
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, classification_report

"""## Data Loading

Tahap untuk memuat dataset yang akan digunakan agar dataset lebih mudah dipahami. Pada project kali ini, menggunakan dataset yang berasal dari Kaggle. [Link Dataset](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset?select=Users.csv)
"""

#!/bin/bash
!curl -L -o book-recommendation.zip\
  "https://www.kaggle.com/api/v1/datasets/download/arashnic/book-recommendation-dataset"

#membuka zip menjadi folder
with zipfile.ZipFile("/content/book-recommendation.zip", "r") as zip_ref:
    zip_ref.extractall("book-recommendation")

books = pd.read_csv('/content/book-recommendation/Books.csv')
users = pd.read_csv('/content/book-recommendation/Users.csv')
ratings = pd.read_csv('/content/book-recommendation/Ratings.csv')

print('Jumlah data buku: ', len(books.ISBN.unique()))
print('Jumlah data user: ', len(users['User-ID'].unique()))
print('Jumlah data rating: ', len(ratings['User-ID']))
print('Jumlah data user yang memberi rating: ', len(ratings['User-ID'].unique()))

books.describe(include='all')

"""**Insight:**

Terdapat data judul buku sebesar 271.360 tetapi yang memiliki judul berbeda (unik) ada 102.022. Hal ini menunjukkan bahwa ada buku yang memiliki judul yang sama.
"""

users.describe(include='all')

"""**Insight:**
Terdapat umur yang tidak masuk akal pada kolom `Age` seperti umur dibawah 5 tahun dan diatas 90 tahun.
"""

ratings.describe(include='all')

"""**Insight:**

Berdasarkan informasi dataset pada sumbernya, kaggle, diketahui bahwa Penilaian buku (Book-Rating) memiliki dua jenis:

- **Eksplisit**:

Penilaian ini diberikan secara langsung oleh pengguna dalam bentuk angka pada skala 1 hingga 10. Semakin tinggi angka yang diberikan, semakin tinggi apresiasi atau kesukaan pengguna terhadap buku tersebut.


- **Implisit**:

Penilaian ini tidak diberikan secara langsung, melainkan ditandai dengan angka 0. Angka 0 ini mengindikasikan bahwa pengguna mungkin telah berinteraksi dengan buku tersebut (misalnya, melihat detailnya, menambahkannya ke daftar bacaan, atau melakukan tindakan lain), tetapi tidak memberikan penilaian eksplisit dalam skala 1-10.
Saya akan fokus membangun model collaborative filtering pada dara rating eksplisit, sehingga data rating implisit nantinya akan dihapus.
"""

books.info()
users.info()
ratings.info()

"""**Insight:**
1. books = Terdapat missing value pada kolom `Book-Author`, `Publisher`, dan `Image-URL-L`.
2. users = Dapat dilihat bahwa terdapat banyak missing value pada kolom `Age`.
3. ratings = tidak terdapat missing value.

## Merge Table
"""

# Menggabungkan ratings dengan users
df = pd.merge(ratings, users, on='User-ID', how='inner')

# Menggabungkan hasil di atas dengan books
df_merged = pd.merge(df, books, on='ISBN', how='inner')

df_merged.info()

"""**Insight**:
dataframe `merged_df`. gabungan antara dataframe `books`, `ratings`, dan `users`

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

## Exploratory Data Analysis

### Distribusi Usia Pembaca
"""

plt.figure(figsize=(10,5))
sns.histplot(df_merged['Age'].dropna(), bins=40, kde=True, color='skyblue')
plt.title('Distribusi Usia Pengguna')
plt.xlabel('Usia')
plt.ylabel('Jumlah')
plt.show()

"""**Insight:**

Berdasarkan histogram tersebut, dapat disimpulkan bahwa mayoritas pengguna dalam dataset ini adalah kalangan dewasa muda, dengan puncak distribusi usia terkonsentrasi secara signifikan antara 20 hingga 40 tahun. Grafik ini juga menunjukkan adanya right-skew (condong ke kanan), yang menandakan bahwa jumlah pengguna secara bertahap menurun seiring bertambahnya usia, meskipun masih ada basis pengguna yang cukup di usia paruh baya. Selain itu, terdapat indikasi kuat adanya data anomali atau outlier pada usia yang sangat rendah (mendekati 0) dan sangat tinggi (jauh di atas 100 tahun), yang mengindikasikan perlunya pembersihan data lebih lanjut sebelum analisis mendalam.

### Distribusi Buku yang Paling Banyak Dinilai
"""

top_books = df_merged['Book-Title'].value_counts().head(10)

plt.figure(figsize=(10,5))
sns.barplot(y=top_books.index, x=top_books.values, palette='magma')
plt.title('Top 10 Buku yang Paling Banyak Dinilai')
plt.xlabel('Jumlah Rating')
plt.ylabel('Judul Buku')
plt.show()

"""**Insight:**

Berdasarkan grafik tersebut, terlihat jelas bahwa popularitas buku diukur dari jumlah rating yang diterima, bukan dari skor rata-ratanya. Buku "Wild Animus" merupakan outlier yang sangat dominan, menerima jumlah ulasan yang hampir dua kali lipat lebih banyak dibandingkan buku di peringkat kedua. Fenomena ini kemungkinan besar tidak murni mencerminkan kualitas buku, melainkan bisa jadi akibat dari kampanye pemasaran atau program bagi-bagi buku gratis yang masif pada masanya, sehingga menghasilkan interaksi yang sangat tinggi dalam dataset ini. Sementara itu, sisa dari daftar top 10 diisi oleh novel-novel fiksi populer dan bestseller yang sangat dikenal pada masanya seperti "The Lovely Bones" dan "The Da Vinci Code", yang mengindikasikan bahwa selera mayoritas pengguna dalam dataset ini cenderung ke arah fiksi komersial yang terkenal.

### Distribusi Penulis dengan Buku Paling Banyak Dirating
"""

top_authors = df_merged['Book-Author'].value_counts().head(10)

plt.figure(figsize=(10,5))
sns.barplot(y=top_authors.index, x=top_authors.values, palette='cividis')
plt.title('Top 10 Penulis Paling Banyak Dirating')
plt.xlabel('Jumlah Rating')
plt.ylabel('Penulis')
plt.show()

"""**Insight:**

Grafik ini mengukuhkan dominasi penulis-penulis fiksi komersial ternama dalam menarik minat baca pengguna, dengan Stephen King secara meyakinkan menempati posisi teratas sebagai penulis yang karyanya paling banyak diulas. Daftar 10 besar ini didominasi secara kuat oleh para penulis 'powerhouse' yang sangat produktif dalam genre spesifik seperti thriller, misteri, dan romance, seperti Nora Roberts, John Grisham, dan James Patterson. Hal ini memberikan sinyal yang sangat jelas bahwa mayoritas pembaca dalam dataset ini memiliki preferensi yang kuat terhadap cerita-cerita yang penuh ketegangan (suspense) dan narasi romantis, di mana popularitas penulis dibangun secara kumulatif dari banyaknya karya yang mereka hasilkan, bukan hanya dari satu buku 'hit'.

### Distribusi Jumlah Rating per Buku
"""

# Hanya rating eksplisit (1-10)
explicit_ratings = df_merged[df_merged['Book-Rating'] >= 0]

plt.figure(figsize=(6,4))
sns.countplot(x='Book-Rating', data=explicit_ratings, palette='Set2')
plt.title('Distribusi Nilai Rating Eksplisit (1-10)')
plt.xlabel('Rating')
plt.ylabel('Jumlah')
plt.show()

"""**Insight:**

Grafik distribusi rating ini menyoroti sebuah karakteristik fundamental dan paling penting dari dataset ini: mayoritas absolut interaksi (lebih dari 600.000) adalah rating '0'. Rating '0' ini bukanlah skor buruk, melainkan sebuah rating implisit, yang kemungkinan besar menandakan bahwa pengguna telah berinteraksi dengan buku tersebut (misalnya, ada di rak bukunya) tetapi tidak memberikan skor numerik secara eksplisit. Jika kita hanya berfokus pada rating eksplisit (skala 1-10), terlihat pola yang sangat berbeda, yaitu pengguna cenderung memberikan ulasan positif dengan jumlah rating yang sangat sedikit di skor rendah (1-4) dan mencapai puncaknya di skor 7 dan 8. Hal ini menunjukkan adanya bias ke arah rating positif untuk ulasan eksplisit dan menegaskan betapa krusialnya untuk memisahkan data implisit ('0') dan eksplisit (1-10) dalam analisis dan pemodelan selanjutnya.

## Data Quality Verification
"""

# Menghitung jumlah nilai null untuk setiap kolom di df_merged
missing_values = df_merged.isnull().sum()

# Menampilkan hasilnya
print(missing_values)

"""**Insight:**

Terdapat missing value pada kolom `Age` sebanyak  277835 atau kurang dari 50% sehingga akan saya hapus data tersebut.
"""

# Menampilkan jumlah pengarang, jumlah penerbit, dan tahun terbit
print('Jumlah Pengarang: ', len(df_merged['Book-Author'].unique()))
print('Jumlah Penerbit: ', len(df_merged['Publisher'].unique()))
print('Tahun Terbit', df_merged['Year-Of-Publication'].unique())

"""**insight:**

Dapat dilihat bahwa pada data tahun masih belum seragam, ada yang menggunakan tanda petik dan ada yang tidak. Selain itu, terdapat data yang salah, yaitu *DK Publishing Inc* dan *Gallimard* yang seharusnya berada pada kolom Publisher (penerbit). Data ini akan dihapus pada bagian Data Preparation.
"""

# Membuat daftar nilai anomali yang ingin dicari
outliner_values = ['DK Publishing Inc', 'Gallimard']

# Mencari semua baris di mana 'Year-Of-Publication' adalah salah satu dari nilai di dalam daftar
books.loc[books['Year-Of-Publication'].isin(outliner_values)]

# Menghitung berapa banyak baris yang merupakan duplikat penuh dari baris sebelumnya
jumlah_duplikat_penuh = df_merged.duplicated().sum()

print(f"Ditemukan {jumlah_duplikat_penuh} jumlah duplikasi data")

df_merged.info()

"""# Data Preparation

## Data Cleaning
"""

# Menghapus nilai yang tetukar
indeks_salah = df_merged[df_merged['Year-Of-Publication'].isin(['DK Publishing Inc', 'Gallimard'])].index

# Hapus baris berdasarkan indeksnya
df_merged.drop(indeks_salah, inplace=True)

# Menghapus kolom Image URL karena tidak digunakan pada analisis
df_merged.drop(['Age','Location','Image-URL-S', 'Image-URL-M', 'Image-URL-L'], axis=1, inplace=True)

# Mengisi nilai yang kosong pada kolom 'Book-Author' dan 'Publisher' dengan 'other'
df_merged['Book-Author'] = df_merged['Book-Author'].fillna('other')
df_merged['Publisher'] = df_merged['Publisher'].fillna('other')

# Cek apakah data telah berhasil diubah menjadi 'other'
df_merged.loc[df_merged['Book-Author'] == 'other', :]

# Pastikan kolom bertipe string dan isi NaN diganti string kosong dulu agar tidak error saat isdigit()
df_merged['Year-Of-Publication'] = df_merged['Year-Of-Publication'].astype(str).fillna('')

# Gunakan .str.isdigit() untuk filter baris dengan tahun valid
df_merged = df_merged[df_merged['Year-Of-Publication'].str.isdigit()]

# Ubah ke integer
df_merged['Year-Of-Publication'] = df_merged['Year-Of-Publication'].astype(int)

# Buang baris dengan tahun tidak masuk akal (misalnya < 1900 atau > 2025)
df_merged = df_merged[(df_merged['Year-Of-Publication'] >= 1900) &
                      (df_merged['Year-Of-Publication'] <= 2025)]

# Ambil hanya data rating eksplisit
ratings_explicit = df_merged[df_merged['Book-Rating'] != 0]

print(f"Jumlah baris sebelum drop implisit: {len(df_merged)}")
print(f"Jumlah baris setelah drop implisit: {len(ratings_explicit)}")

df_merged = ratings_explicit

print("Tahun unik setelah dibersihkan:", sorted(df_merged['Year-Of-Publication'].unique()))

df_merged.duplicated().sum()

df_merged.duplicated(subset=['User-ID', 'ISBN']).sum()

df_merged = df_merged.reset_index(drop=True)
print(df_merged.info())

df_merged.describe(include='all')

df_merged.isnull().sum()

# Membuat dictionary untuk data 'book_id', 'title', 'author', dan 'publisher'
book_new = books.rename(columns={
    'ISBN': 'id',
    'Book-Title': 'book_title',
    'Book-Author': 'book_author',
    'Publisher': 'publisher'
})[['id', 'book_title', 'book_author', 'publisher']]

"""## Encoding dan Data Splitting"""

df_model = df_merged[['User-ID', 'ISBN', 'Book-Rating']].copy()
df_model = df_model.rename(columns={'User-ID': 'user_id', 'ISBN': 'isbn', 'Book-Rating': 'rating'})

# Mengubah user_id menjadi list tanpa nilai yang sama
user_ids = df_model['user_id'].unique().tolist()
print('list user_id: ', user_ids)

# Melakukan encoding user_id
user_to_user_encoded = {x: i for i, x in enumerate(user_ids)}
print('encoded user_id : ', user_to_user_encoded)

# Melakukan proses encoding angka ke user_id
user_encoded_to_user = {i: x for i, x in enumerate(user_ids)}
print('encoded angka ke user_id: ', user_encoded_to_user)

# Mengubah isbn menjadi list tanpa nilai yang sama
book_ids = df_model['isbn'].unique().tolist()

# Melakukan proses encoding isbn
book_to_book_encoded = {x: i for i, x in enumerate(book_ids)}

# Melakukan proses encoding angka ke isbn
book_encoded_to_book = {i: x for i, x in enumerate(book_ids)}

df_model['user'] = df_model['user_id'].map(user_to_user_encoded)
df_model['book'] = df_model['isbn'].map(book_to_book_encoded)

# Mendapatkan jumlah user
num_users = len(user_to_user_encoded)
print(num_users)

# Mendapatkan jumlah buku
num_books = len(book_encoded_to_book)
print(num_books)

# Mengubah rating menjadi nilai float
df_model['rating'] = df_model['rating'].values.astype(np.float32)

# Nilai minimum rating
min_rating = df_model['rating'].min()

# Nilai maksimal rating
max_rating = df_model['rating'].max()

print('Number of User: {}, Number of Book: {}, Min Rating: {}, Max Rating: {}'.format(
    num_users, num_books, min_rating, max_rating
))

# Mengacak dataset
df_model = df_model.sample(frac=1, random_state=42)
df_model

# Membuat variabel x untuk mencocokkan data user dan book menjadi satu value (pakai df_model yang sudah shuffle)
x = df_model[['user', 'book']].values

# Membuat variabel y dengan rating yang sudah dinormalisasi
y = df_model['rating'].apply(lambda x: (x - min_rating) / (max_rating - min_rating)).values

# Membagi menjadi 80% data train dan 20% data validasi
train_indices = int(0.8 * df_model.shape[0])
x_train, x_val = x[:train_indices], x[train_indices:]
y_train, y_val = y[:train_indices], y[train_indices:]

print(x_train.shape, y_train.shape)
print(x_val.shape, y_val.shape)

"""# Modeling and Result

## Collaborative Filtering
"""

class RecommenderNet(tf.keras.Model):

  # Insialisasi fungsi
  def __init__(self, num_users, num_book, embedding_size, **kwargs):
    super(RecommenderNet, self).__init__(**kwargs)
    self.num_users = num_users
    self.num_book = num_book
    self.embedding_size = embedding_size
    self.user_embedding = layers.Embedding( # layer embedding user
        num_users,
        embedding_size,
        embeddings_initializer = 'he_normal',
        embeddings_regularizer = keras.regularizers.l2(1e-6)
    )
    self.user_bias = layers.Embedding(num_users, 1) # layer embedding user bias
    self.book_embedding = layers.Embedding( # layer embeddings book
        num_book,
        embedding_size,
        embeddings_initializer = 'he_normal',
        embeddings_regularizer = keras.regularizers.l2(1e-6)
    )
    self.book_bias = layers.Embedding(num_book, 1) # layer embedding book bias

  def call(self, inputs):
    user_vector = self.user_embedding(inputs[:,0]) # memanggil layer embedding 1
    user_bias = self.user_bias(inputs[:, 0]) # memanggil layer embedding 2
    book_vector = self.book_embedding(inputs[:, 1]) # memanggil layer embedding 3
    book_bias = self.book_bias(inputs[:, 1]) # memanggil layer embedding 4

    dot_user_book = tf.tensordot(user_vector, book_vector, 2)

    x = dot_user_book + user_bias + book_bias

    return tf.nn.sigmoid(x)

model = RecommenderNet(num_users, num_books, 20)  # inisialisasi model

model.compile(
    loss=tf.keras.losses.MeanSquaredError(),
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    metrics=[tf.keras.metrics.RootMeanSquaredError()]
)

from tensorflow.keras.callbacks import EarlyStopping
early_stop = EarlyStopping(
    monitor='val_root_mean_squared_error',  # metric yang kamu pakai di compile
    patience=5,                            # berapa epoch tanpa perbaikan sebelum stop
    restore_best_weights=True              # kembalikan bobot terbaik setelah training selesai
)

history = model.fit(
    x=x_train,
    y=y_train,
    batch_size=32,
    epochs=100,
    validation_data=(x_val, y_val),
    callbacks=[early_stop]
)

"""**Insight:**

1. Konsistensi Penurunan Loss dan RMSE pada Data Training

- Model menunjukkan performa yang baik dalam mempelajari pola dari data training.

- Terlihat dari penurunan metrik loss dari 0.0759 (RMSE: 0.2732) di epoch 1 menjadi 0.0209 (RMSE: 0.1406) di epoch 14.


2. Val_loss dan Val_RMSE Mengalami Perbaikan Terbatas

- Pada awal training (epoch 1), val_loss dan val_RMSE tercatat 0.0418 dan 0.1984.

- Di akhir epoch ke-14, hanya turun sedikit menjadi 0.0371 dan 0.1897.

3. Stabilitas Waktu Training

- Rata-rata durasi tiap epoch berada di kisaran 30–40 detik, menunjukkan proses training berjalan efisien dan konsisten.

- Tidak ada fluktuasi signifikan dalam waktu proses, sehingga tidak ditemukan bottleneck dari sisi performa komputasi.
"""

plt.plot(history.history['root_mean_squared_error'])
plt.plot(history.history['val_root_mean_squared_error'])
plt.title('model_metrics')
plt.ylabel('root_mean_squared_error')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

"""**Insight;**

Dari grafik RMSE terlihat bahwa training error terus menurun, menunjukkan model semakin baik mempelajari data training. Namun, validation error awalnya turun lalu stabil dan sedikit naik, menandakan model sudah mencapai batas generalisasi pada data validasi. Terdapat gap antara training dan validation error yang menunjukkan model mulai overfitting. Disarankan untuk menggunakan early stopping, teknik regularisasi seperti dropout atau L2, serta melakukan tuning hyperparameter dan menambah data jika memungkinkan untuk mengurangi overfitting dan meningkatkan performa.
"""

def precision_recall_at_k(model, x_val, y_val, k=10):
    # Asumsikan x_val bentuknya [user_id, book_id], dan y_val adalah rating sebenarnya
    hit = 0
    total_recommended = 0
    total_relevant = 0

    user_ids = np.unique(x_val[:, 0])

    for user_id in user_ids:
        # Ambil semua data val user ini
        idx = x_val[:, 0] == user_id
        books = x_val[idx, 1]
        ratings_true = y_val[idx]

        if len(books) < k:
            continue

        # Prediksi untuk semua buku milik user ini
        input_pairs = np.hstack((np.full((len(books), 1), user_id), books.reshape(-1, 1)))
        preds = model.predict(input_pairs).flatten()

        # Ambil Top-K
        top_k_idx = preds.argsort()[-k:][::-1]
        recommended_ratings = ratings_true[top_k_idx]

        # Asumsikan rating > 0.5 adalah relevan
        hit += np.sum(recommended_ratings >= 0.5)
        total_recommended += k
        total_relevant += np.sum(ratings_true >= 0.5)

    precision = hit / total_recommended
    recall = hit / total_relevant
    return precision, recall

precision, recall = precision_recall_at_k(model, x_val, y_val, k=10)
print(f"Precision@10: {precision:.4f}")
print(f"Recall@10: {recall:.4f}")

"""**Insight:**
Precision@10 sebesar 87.98% menunjukkan bahwa dari setiap 10 rekomendasi yang diberikan, sekitar 8 hingga 9 item benar-benar relevan dengan preferensi user. Ini menandakan model sangat akurat dalam memilih rekomendasi yang tepat.

Sementara itu, Recall@10 sebesar 41.73% berarti dari semua item relevan yang ada untuk setiap user, sekitar 41% berhasil masuk dalam 10 rekomendasi teratas. Angka ini cukup baik dan wajar mengingat rekomendasi hanya dibatasi pada Top-10, sedangkan total item relevan bisa jauh lebih banyak.

# Evaluation

## Metrik Evaluasi

**Root Mean Squared Error (RMSE)**

RMSE mengukur seberapa besar perbedaan (*error*) antara rating prediksi dan rating aktual dari pengguna. Metrik ini cocok digunakan pada sistem rekomendasi berbasis rating eksplisit, seperti dalam proyek ini.

**Rumus:**

$$
\text{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (\hat{r}_i - r_i)^2}
$$

Dimana:  
- $\hat{r}_i$ : rating prediksi dari model  
- $r_i$ : rating aktual dari pengguna  
- $n$ : jumlah data  


**Cara kerja:**  
Semakin kecil nilai RMSE, semakin kecil selisih antara rating prediksi dan aktual → berarti model lebih akurat.

**Precision@K dan Recall@K**

Metrik ini digunakan untuk mengevaluasi performa sistem rekomendasi dalam hal *relevansi* terhadap item (buku) yang direkomendasikan.

**Precision@K**

Mengukur proporsi item yang **relevan** dari total \(K\) item yang direkomendasikan.

$$
\text{Precision@K} = \frac{\text{Jumlah item relevan di top-}K}{K}
$$

**Recall@K**

Mengukur proporsi item relevan yang berhasil direkomendasikan dari seluruh item relevan yang tersedia.

$$
\text{Recall@K} = \frac{\text{Jumlah item relevan di top-}K}{\text{Total item relevan}}
$$


## Interpretasi dan Insight dari Evaluasi

1. RMSE Insight:
- Jika grafik RMSE validasi menurun dan stabil, itu menunjukkan model belajar dengan baik.

- Gap besar antara RMSE training dan validasi → bisa jadi overfitting.

2. Precision & Recall Insight:
- Tinggi precision berarti rekomendasi yang diberikan relevan.

- Recall moderat menunjukkan model bisa ditingkatkan lagi untuk menemukan lebih banyak item relevan.

- Bisa jadi model terlalu konservatif (memilih item yang sudah populer), sehingga tidak mengeksplor banyak opsi relevan lainnya.

# Menjawab Problems

## 1. Mengidentifikasi buku, penulis, dan karakteristik lainnya yang paling sering mendapatkan rating dari pengguna, berdasarkan analisis data rating eksplisit.
"""

# Hitung jumlah rating per judul buku
top_rated_books = df_merged.groupby(['Book-Title', 'Book-Author']).size().reset_index(name='Jumlah_Rating')

# Ambil N teratas (misal: 10 buku paling banyak diberi rating)
top_n = top_rated_books.sort_values(by='Jumlah_Rating', ascending=False).head(10)

# Visualisasi
plt.figure(figsize=(12, 6))
sns.barplot(data=top_n, x='Jumlah_Rating', y='Book-Title', hue='Book-Author', dodge=False, palette='viridis')

plt.xlabel("Jumlah Rating yang Diberikan")
plt.ylabel("Judul Buku")
plt.title("10 Buku dengan Jumlah Rating Terbanyak")
plt.legend(title='Penulis', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

"""## 2. Membangun sebuah model sistem rekomendasi fungsional yang memberikan saran bacaan baru yang dipersonalisasi untuk setiap pengguna."""

import numpy as np
import pandas as pd

# Ambil satu user secara random dari df_model
user_id = df_model['user_id'].sample(1).iloc[0]

# Ambil buku yang sudah dirating user ini
book_rated_by_user = df_model[df_model['user_id'] == user_id]

# Buku yang belum dirating user
all_books = set(df_model['isbn'].unique())
rated_books = set(book_rated_by_user['isbn'].unique())
books_not_rated = list(all_books - rated_books)

# Filter buku yang ada di encoding
books_not_rated = [b for b in books_not_rated if b in book_to_book_encoded]

# Buat array input model: pasangan [user_encoded, book_encoded]
user_encoded = user_to_user_encoded[user_id]
book_encoded_list = [book_to_book_encoded[b] for b in books_not_rated]

user_array = np.array([user_encoded] * len(book_encoded_list))
book_array = np.array(book_encoded_list)
user_book_array = np.column_stack((user_array, book_array))

# Prediksi rating untuk buku yang belum dirating
predicted_ratings = model.predict(user_book_array).flatten()

# Ambil top 10 buku dengan rating tertinggi
top_k = 10
top_k_indices = predicted_ratings.argsort()[-top_k:][::-1]
recommended_books_encoded = [book_encoded_list[i] for i in top_k_indices]

# Mapping ke id buku asli
recommended_books = [book_encoded_to_book[b] for b in recommended_books_encoded]

print(f"Rekomendasi untuk user_id: {user_id}\n")

# Ambil top 5 buku yang sudah dirating user, urutkan berdasarkan rating tertinggi
top_rated_books = book_rated_by_user.sort_values('rating', ascending=False).head(5)

# Hitung rata-rata rating per buku dari data rating yang ada
avg_rating_per_book = df_model.groupby('isbn')['rating'].mean().reset_index()
avg_rating_per_book.rename(columns={'rating': 'Rata-rata Rating'}, inplace=True)

# Buat dataframe buku sudah dirating user dengan judul asli, author, publisher
rated_books_list = []
for _, row in top_rated_books.iterrows():
    book_info = book_new[book_new['id'] == row['isbn']]
    if not book_info.empty:
        title = book_info.iloc[0]['book_title']
        author = book_info.iloc[0]['book_author']
        publisher = book_info.iloc[0]['publisher']
    else:
        title = author = publisher = "Tidak Diketahui"
    rated_books_list.append({
        'ISBN': row['isbn'],
        'Judul': title,
        'Penulis': author,
        'Penerbit': publisher,
        'Rating User': row['rating']
    })

df_rated = pd.DataFrame(rated_books_list)

# Buat dataframe rekomendasi buku baru dengan judul, author, publisher dan rata-rata rating
recommended_books_list = []
for isbn in recommended_books:
    book_info = book_new[book_new['id'] == isbn]
    if not book_info.empty:
        title = book_info.iloc[0]['book_title']
        author = book_info.iloc[0]['book_author']
        publisher = book_info.iloc[0]['publisher']
    else:
        title = author = publisher = "Tidak Diketahui"

    avg_rating_row = avg_rating_per_book[avg_rating_per_book['isbn'] == isbn]
    avg_rating = round(avg_rating_row['Rata-rata Rating'].values[0], 2) if not avg_rating_row.empty else "N/A"

    recommended_books_list.append({
        'ISBN': isbn,
        'Judul': title,
        'Penulis': author,
        'Penerbit': publisher,
        'Rata-rata Rating': avg_rating
    })

df_recommended = pd.DataFrame(recommended_books_list)

# Tampilkan hasil
print("Buku yang sudah dirating user (top 5):")
print(df_rated.to_string(index=False))

print("\nRekomendasi buku cocok untuk dibaca selanjutnya:")
print(df_recommended.to_string(index=False))

"""Daftar Referensi:

[1] Saputra, V. S., Ridwan, A., & Pratama, T. G. (2025).
"Rancang Bangun Sistem Rekomendasi Buku Berbasis Item-Based Collaborative Filtering Menggunakan Algoritma K-Nearest Neighbors."
Jurnal JUST IT, Vol. 15, No. 2, pp. 325–331, Universitas Muhammadiyah Kudus.
[Penelitian ini membahas sistem rekomendasi buku dengan collaborative filtering berbasis K-NN dan evaluasi menggunakan MAE serta RMSE].

[2] Fathoni, M. (2023).
"Sistem Rekomendasi Buku di Perpustakaan Daerah Jepara Menggunakan Metode Item-Based Collaborative Filtering."
Jurnal Biner, Universitas Sains Al-Qur'an.
[Studi kasus penerapan collaborative filtering di perpustakaan daerah dengan evaluasi MAE].

[3] ‘Uyun, S., Fahrurozzi, I., & Mulyanto, A. (2020).
"Item Collaborative Filtering untuk Rekomendasi Pembelian Buku secara Online."
Jurnal Sistem Informasi, Universitas Ahmad Dahlan.
[Pengembangan sistem rekomendasi pada toko buku online dengan collaborative filtering].

[4] Tim Jurnal Ilmu Komputer dan Sistem Informasi, Universitas Tarumanagara (2024).
"Implementasi Metode Collaborative Filtering Based Untuk Sistem Rekomendasi Buku."
JIKSI, Universitas Tarumanagara.
[Analisis collaborative filtering dalam sistem rekomendasi buku dan evaluasi akurasi menggunakan MAE].


"""