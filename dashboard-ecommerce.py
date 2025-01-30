import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def cre_top_products(df):
    # Kelompokkan berdasarkan product_id untuk hitung total transaksi
    top_products = (
    df.groupby('product_category_name')
    .agg(
        total_sold=('order_id', 'size'),  # Hitung total transaksi per produk
        avg_price=('price', 'mean'),       # Rata-rata harga produk
    )
    .sort_values(by='total_sold', ascending=False)  # Urutkan berdasarkan total penjualan
    .reset_index()
    .nlargest(10, 'total_sold')
)
    return top_products

def cre_last_transcation(df):
    # Menentukan tanggal transaksi terakhir per pelanggan
    last_transaction = df.groupby('customer_id')['order_purchase_timestamp'].max().reset_index()
    # Tentukan tanggal referensi, misalnya tanggal terakhir dalam dataset
    reference_date = df['order_purchase_timestamp'].max()
    # Menghitung Recency (hari sejak transaksi terakhir)
    last_transaction['recency'] = (reference_date - last_transaction['order_purchase_timestamp']).dt.days
    
    return last_transaction, reference_date

def cre_rfm(df):
    # Menggabungkan Recency dengan Frequency dan Monetary
    rfm = pd.merge(last_transaction_date[['customer_id', 'recency']],
                   df.groupby('customer_id').agg(
                       frequency=('order_id', 'count'),
                       monetary=('payment_value', 'sum')
                   ).reset_index(),
                   on='customer_id')
    
    # Menentukan kuantil untuk setiap metrik RFM
    rfm['recency_score'] = pd.qcut(rfm['recency'], 4, labels=[4, 3, 2, 1])
    rfm['frequency_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4])
    rfm['monetary_score'] = pd.qcut(rfm['monetary'], 4, labels=[1, 2, 3, 4])

    # Total Skor RFM
    rfm['rfm_score'] = rfm['recency_score'].astype(int) + rfm['frequency_score'].astype(int) + rfm['monetary_score'].astype(int)
    
    # Klasifikasi RFM
    def classify_rfm(row):
        if row['rfm_score'] >= 10:
            return 'Best Customers'
        elif 7 <= row['rfm_score'] <= 9:
            return 'Loyal Customers'
        elif 4 <= row['rfm_score'] <= 6:
            return 'Potential Loyalists'
        elif 1 <= row['rfm_score'] <= 3:
            return 'At-Risk Customers'
        else:
            return 'Lost Customers'

    rfm['customer_segment'] = rfm.apply(classify_rfm, axis=1)
    
    return rfm

def classify_review(score):
    if score in [1, 2]:
        return 'Tidak Puas'
    elif score == 3:
        return 'Netral'
    else:
        return 'Puas'

# df = pd.read_csv("C:/Users/agivc/Documents/PELATIHAN IDCAMP DATA SCIENTIST/Proyek Analisis Data (E-Commerce)/e-commerce_analysis.csv")
df = pd.read_csv("e-commerce_analysis.csv")
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
top_products = cre_top_products(df)
#Menghitung tren penjualan produk terlaris
categories = top_products['product_category_name'].tolist()

# Konversi kolom tanggal jika belum dilakukan
df['order_purchase_month'] = pd.to_datetime(df['order_purchase_timestamp']).dt.to_period('M')

last_transaction_date, reference_date = cre_last_transcation(df)

rfm = cre_rfm(df)
df['satisfaction_category'] = df['review_score'].apply(classify_review)
satisfaction_distribution = df['satisfaction_category'].value_counts(normalize=True) * 100
# Menghitung jumlah pelanggan di setiap segmen RFM
segment_counts_cust = rfm['customer_segment'].value_counts()
review_distribution = df['review_score'].value_counts(normalize=True).sort_index() * 100

st.header('E-Commerce Analysis')
st.caption('Proyek Akhir Kelas Data Analisis Dicoding')

st.subheader('Produk Paling Laris dan Tidak Laris Terjual')
# Pilihan jumlah data yang ingin ditampilkan
num_products = st.slider("Pilih jumlah produk untuk ditampilkan", min_value=1, max_value=len(top_products), value=5)

# Plot grafik
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(30, 15))

# Plot Best Performing Product
sns.barplot(
    x="total_sold", 
    y="product_category_name", 
    data=top_products.head(num_products), 
    palette='viridis', 
    ax=ax[0]
)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Best Performing Product", loc="center", fontsize=25)
ax[0].tick_params(axis='y', labelsize=20)

# Plot Worst Performing Product
sns.barplot(
    x="total_sold", 
    y="product_category_name", 
    data=top_products.sort_values(by="total_sold", ascending=True).head(num_products), 
    palette='viridis', 
    ax=ax[1]
)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=25)
ax[1].tick_params(axis='y', labelsize=20)

# Tampilkan plot
st.pyplot(fig)

st.subheader('Tren Penjualan 10 Produk Terlaris')
# Memilih kategori produk
selected_category = st.selectbox('Pilih Kategori Produk', categories)
#Filter tren penjualan bulanan untuk kategori yang dipilih
trend = df[df['product_category_name'] == selected_category] \
    .groupby('order_purchase_month')['order_id'].size()
# Plot tren penjualan
fig, ax = plt.subplots(figsize=(18, 6))
trend.plot(marker='o', title=f'Tren Penjualan Bulanan: {selected_category}', ax=ax)
plt.ylabel('Total Penjualan')
plt.xlabel('Bulan')
plt.grid(True)

# Tampilkan plot
st.pyplot(fig)


st.subheader('Distribusi Transaksi Pelanggan Berdasarkan Recency')
# Tentukan ambang batas Recency untuk segmentasi
active_threshold = 365  # Pelanggan yang terakhir bertransaksi dalam 365 hari dianggap aktif

# Segmentasi Pelanggan Berdasarkan Recency
last_transaction_date['segment'] = last_transaction_date['recency'].apply(
    lambda x: 'Aktif' if x <= active_threshold else 'Tidak Aktif'
)

# Cek distribusi Recency berdasarkan segmentasi
active_customers = last_transaction_date[last_transaction_date['segment'] == 'Aktif']
inactive_customers = last_transaction_date[last_transaction_date['segment'] == 'Tidak Aktif']

# Menyiapkan figure dengan dua subplot (1 baris, 2 kolom)
fig, ax = plt.subplots(1, 2, figsize=(26, 12))

# Visualisasi Distribusi Recency per Segmen (Histogram) di subplot pertama
sns.histplot(active_customers['recency'], kde=True, color='lightgreen', bins=40, label='Pelanggan Aktif', ax=ax[0])
sns.histplot(inactive_customers['recency'], kde=True, color='salmon', bins=40, label='Pelanggan Tidak Aktif', ax=ax[0])
ax[0].set_title('Distribusi Recency Berdasarkan Segmentasi Pelanggan', fontsize=25)
ax[0].set_xlabel(f'Hari Sejak Transaksi Terakhir: {reference_date.strftime("%Y-%m-%d")}', fontsize=25)
ax[0].set_ylabel('Frekuensi', fontsize=25)
ax[0].legend(fontsize=25)
ax[0].tick_params(axis='both', which='major', labelsize=20)
ax[0].grid(True)

# Visualisasi Pie Chart untuk perbandingan Pelanggan Aktif dan Tidak Aktif di subplot kedua
segment_counts = last_transaction_date['segment'].value_counts()
labels = [f"{segment_counts.index[i]} ({segment_counts[i]})" for i in range(len(segment_counts))]  # Menambahkan jumlah pelanggan pada label
ax[1].pie(segment_counts, labels=labels, autopct='%1.1f%%', startangle=90, colors=['lightgreen', 'salmon'], textprops={'fontsize':25})
ax[1].set_title('Perbandingan Pelanggan Aktif dan Tidak Aktif', fontsize=25)
ax[1].axis('equal')  # Membuat chart bulat
# Menampilkan plot
plt.tight_layout()
st.pyplot(fig)


st.subheader('Segmentasi Pelanggan yang Berpotensi Mendapat Promo Khusus')
# Warna pastel atau soft tone
colors = ['#FFCC80', '#90CAF9', '#A5D6A7', '#FFAB91', '#BDBDBD']

fig, ax = plt.subplots(figsize=(6, 8))  # Buat figure dan axis
wedges, texts, autotexts = ax.pie(
    segment_counts_cust,
    autopct='%1.1f%%',
    startangle=140,
    colors=colors,
    labels=segment_counts_cust.index,
    wedgeprops={'edgecolor': 'white'},  # Garis tepi antar segmen
    textprops={'fontsize': 25},  # Ukuran font label
    pctdistance=0.85
)

# Styling teks presentase di dalam pie chart
for autotext in autotexts:
    autotext.set_color('black')  # Warna teks hitam
    autotext.set_fontsize(20)  # Perbesar ukuran font
    autotext.set_weight('bold')  # Tebalkan teks

# Styling label segmen di luar pie chart
for text in texts:
    text.set_fontsize(12)
    text.set_bbox(dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.3'))

# Atur judul agar lebih rapi dan di tengah
ax.set_title('Proporsi Segmen Pelanggan', fontsize=20, pad=20)

ax.set_ylabel('')  # Hapus label sumbu Y

# Tampilkan pie chart di Streamlit
st.pyplot(fig)


st.subheader('Distribusi Tingkat Kepuasan Pelanggan Terhadap E-Commerce')
# Setup untuk layout dengan 1 row dan 2 kolom
fig, axes = plt.subplots(1, 2, figsize=(16, 6), gridspec_kw={'width_ratios': [1, 1]})

# **Bar Plot untuk Distribusi Skor Ulasan**
sns.barplot(ax=axes[0], x=review_distribution.index, y=review_distribution.values, palette="viridis")
axes[0].set_title('Distribusi Tingkat Kepuasan Pelanggan Berdasarkan Review Score', fontsize=14)
axes[0].set_xlabel('Skor Ulasan (Review Score)', fontsize=12)
axes[0].set_ylabel('Persentase (%)', fontsize=12)
axes[0].set_ylim(0, 100)

# **Pie Chart untuk Distribusi Kategori Tingkat Kepuasan**
colors = sns.color_palette("coolwarm", len(satisfaction_distribution))
axes[1].pie(
    satisfaction_distribution.values, 
    labels=satisfaction_distribution.index, 
    autopct='%1.1f%%', 
    startangle=90, 
    colors=colors
)
axes[1].set_title('Distribusi Kategori Tingkat Kepuasan', fontsize=14)

# **Tampilkan Plot**
plt.tight_layout()
st.pyplot(fig)