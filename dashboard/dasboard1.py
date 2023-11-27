import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe

def create_weathersit_df(df):
    weathersit_df = df.groupby('weathersit')['cnt'].sum().reset_index()
    return weathersit_df

def create_monthly_trend_df(df):
    # Mengelompokkan data berdasarkan bulan dan menghitung jumlah peminjaman setiap bulan
    monthly_trend_df = df.resample('M', on='dteday')['cnt'].sum().reset_index()

    # Merubah format 'dteday' menjadi bulan-tahun
    monthly_trend_df['dteday'] = monthly_trend_df['dteday'].dt.strftime('%b-%Y')
    return monthly_trend_df

def create_weekday_df(df):
    # Mengelompokkan data berdasarkan weekday
    weekday_df = df.groupby('weekday').agg({
    'cnt':['sum'],
    'registered':['sum'],
    'casual':['sum']
    
    })
    return weekday_df

def create_workingday_df(df):    
    # Mengelompokkan data berdasarkan working day
    workingday_df = df.groupby('workingday').agg({
    'cnt':['sum'],
    'registered':['sum'],
    'casual':['sum']
    
    })
    return workingday_df

def create_seasonal_trend_df(df):
    # Mengelompokkan data berdasarkan musim dan menghitung jumlah peminjaman setiap musim
    seasonal_trend_df = df.groupby('season')['cnt'].sum().reset_index()
    return seasonal_trend_df


# Load cleaned data
day_df = pd.read_csv("day.csv")

datetime_columns = ["dteday"]
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)

for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])

# Filter data
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo 
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    #st.image('bike.png')
    
    # Mengambil start_date & end_date dari date_input sebagai tuple
    date_range = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date)
    )

# Mengonversi objek tanggal menjadi datetime
start_date, end_date = pd.to_datetime(date_range)

main_df = day_df[(day_df["dteday"] >= start_date) & (day_df["dteday"] <= end_date)]

# Menyiapkan berbagai dataframe
weathersit_df = create_weathersit_df(main_df)
monthly_trend_df = create_monthly_trend_df(main_df)
weekday_df = create_weekday_df(main_df)
workingday_df = create_workingday_df(main_df)
seasonal_trend_df = create_seasonal_trend_df(main_df)

# # Plot tren bulanan
st.header('Dicoding Bike Sharing Dashboard :sparkles:')
st.subheader('Trend Peminjaman Sepeda Bulanan')

col1, col2 = st.columns(2)

with col1:
    total_regist = main_df.registered.sum()
    st.metric("Total Pengguna Terdaftar", value=total_regist)

with col2:
    total_casual = main_df.casual.sum() 
    st.metric("Total Pengguna Casual", value=total_casual)

plt.figure(figsize=(10, 6))
plt.plot(monthly_trend_df['dteday'], monthly_trend_df['cnt'], marker='o', linestyle='-')
plt.xlabel('Bulan-Tahun')
plt.ylabel('Jumlah Peminjaman')
plt.xticks(rotation=45)  # Rotasi label bulan-tahun
plt.grid(True)
st.pyplot(plt.gcf())

# Buat plot untuk weathersit_df (untuk mengetahui pengaruh cuaca terhadap jumlah peminjaman)
st.subheader('Peminjaman Sepeda Berdasarkan Cuaca')
plt.figure(figsize=(8, 6))
sns.barplot(x='weathersit', y='cnt', data=weathersit_df)
plt.xlabel('Kondisi Cuaca')
plt.ylabel('Total Peminjaman')
# Mengubah label sumbu x
plt.xticks(ticks=[0, 1, 2, 3], labels=['Clear', 'Cloudy', 'Light Rain', 'Heavy Rain'])

# Menampilkan plot di Streamlit
st.pyplot(plt.gcf())

# Membuat plot pengguna weekday berdasarkan tipe pengguna (casual & registered)
st.subheader('Peminjaman Sepeda per Hari Berdasar tipe Pengguna')

# Memilih data dari DataFrame
casual_data = weekday_df['casual']['sum']
registered_data = weekday_df['registered']['sum']
index = ['Not Working Day', 'Working Day']

# Mengatur lebar bar
bar_width = 0.35

# Menyiapkan posisi bar
bar_positions1 = range(len(casual_data))
bar_positions2 = [pos + bar_width for pos in bar_positions1]

# Membuat bar plot
fig, ax = plt.subplots()
ax.bar(bar_positions1, casual_data, width=bar_width, label='Casual', alpha=0.7)
ax.bar(bar_positions2, registered_data, width=bar_width, label='Registered', alpha=0.7)

# Menandai sumbu dan judul
ax.set_xlabel('Day of Week')
ax.set_ylabel('Total Users')
ax.set_title('Total Users by Day of Week')

# Menambahkan legenda
ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

# Mengubah label sumbu x
ax.set_xticks(ticks=[0, 1, 2, 3, 4, 5, 6])
ax.set_xticklabels(['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'])

# Menampilkan plot di Streamlit
st.pyplot(fig)

# Membuat PLot pengguna saat weekend & holiday Vs working day berdasarkan tipe pengguna
st.subheader('Pengguna Weekend & Holiday VS Working Day Berdasar tipe Pengguna')
# Memilih data dari DataFrame
casual_data = workingday_df['casual']['sum']
registered_data = workingday_df['registered']['sum']
index = ['Weekend and Holiday', 'Working Day']

# Mengatur lebar bar
bar_width = 0.35

# Menyiapkan posisi bar
bar_positions1 = range(len(casual_data))
bar_positions2 = [pos + bar_width for pos in bar_positions1]

# Membuat bar plot
fig, ax = plt.subplots()
ax.bar(bar_positions1, casual_data, width=bar_width, label='Casual', alpha=0.7)
ax.bar(bar_positions2, registered_data, width=bar_width, label='Registered', alpha=0.7)

# Menambahkan angka pengguna pada bar
for i, data in enumerate(casual_data):
    ax.text(i, data + 100, str(data), ha='center', va='bottom', fontsize=10)

for i, data in enumerate(registered_data):
    ax.text(i + bar_width, data + 100, str(data), ha='center', va='bottom', fontsize=10)

# Menandai sumbu dan judul
ax.set_xlabel('Day Type')
ax.set_ylabel('Total Users')
ax.set_title('Total Users by Day Type')

# Menandai sumbu x
ax.set_xticks([pos + bar_width/2 for pos in bar_positions1])
ax.set_xticklabels(index)

# Menambahkan legenda
ax.legend()

# Menampilkan plot di Streamlit
st.pyplot(fig)



# Plot tren berdasarkan musim (seasonal_trend_df)
st.subheader('Tren Peminjaman Sepeda Berdasarkan Musim')
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['springgreen', 'skyblue', 'gold', 'firebrick']
bars = ax.bar(seasonal_trend_df['season'], seasonal_trend_df['cnt'], color=colors)
ax.set_title('Tren Peminjaman Sepeda Berdasarkan Musim')
ax.set_xlabel('Musim')
ax.set_ylabel('Jumlah Peminjaman')
ax.grid(True, axis='y')

# Mengubah label sumbu x
ax.set_xticks([1, 2, 3, 4])
ax.set_xticklabels(['spring', 'summer', 'fall', 'winter'])

# Menambahkan label angka pada setiap bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

# Menampilkan plot di Streamlit
st.pyplot(fig)
