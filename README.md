# Dashboard Analisis E-Commerce

## Setup Environment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run steamlit app
```
streamlit run dashboard-ecommerce.py
```

## Link Dashboard
https://dashboard-ecommerce-dc.streamlit.app/

## Pertanyaan untuk Analisis
- Produk apa yang paling laris terjual?
- Bagaimana distribusi waktu terakhir pelanggan bertransaksi?
- Bagaimana segmentasi pelanggan dapat digunakan untuk menentukan target promosi khusus?
- Bagaimana distribusi tingkat kepuasan pelanggan terhadap pengalaman berbelanja di platform e-commerce?

## Kesimpulan
1. Produk Terlaris

    - Produk dengan kategori cama_mesa_banho, beleza_saude, esporte_lazer, moveis_decoracao, dan informatica_acessorios adalah produk yang paling laris, menunjukkan daya tarik yang besar di pasar.
    - Sebaliknya, kategori seperti seguros_e_servicos, fashion_e_servicos, dan cds_dvds_musicais memiliki penjualan rendah, yang perlu dievaluasi lebih lanjut untuk pengelolaan stok dan strategi pemasaran.

2. Distribusi Waktu Terakhir Transaksi

    - Mayoritas pelanggan melakukan transaksi dalam 1-3 bulan terakhir, yang mencerminkan basis pelanggan aktif dan kecenderungan belanja yang konsisten.
    - Pelanggan yang tidak bertransaksi dalam waktu lebih lama dapat menjadi target kampanye reaktivasi untuk meningkatkan retensi.

3. Segmentasi Pelanggan untuk Promosi Khusus

    Segmentasi pelanggan berdasarkan perilaku belanja menunjukkan distribusi berikut:
    - 49,6% pelanggan loyal (Loyal Customers), yang harus dipertahankan dengan program penghargaan atau diskon eksklusif.
    - 31,3% pelanggan potensial (Potential Loyalists), yang membutuhkan insentif untuk meningkatkan loyalitas.
    - 16,8% pelanggan terbaik (Best Customers), yang berkontribusi signifikan pada pendapatan platform.
    - 1,7% pelanggan berisiko (At-Risk Customers), yang memerlukan perhatian khusus untuk kembali bertransaksi.
   
4. Distribusi Tingkat Kepuasan Pelanggan

    - Sebanyak 75,5% pelanggan puas atau sangat puas dengan pengalaman belanja, mencerminkan kepuasan yang tinggi terhadap layanan platform.
    - 16,1% pelanggan bersikap netral, yang menjadi peluang untuk meningkatkan pengalaman belanja agar lebih menarik.
    - 8,4% pelanggan tidak puas atau sangat tidak puas, menandakan aspek yang perlu diperbaiki, seperti kualitas produk, pengiriman, atau layanan pelanggan.
