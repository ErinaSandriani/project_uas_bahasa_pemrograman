import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ======================
# FILE PATH
# ======================
BARANG_FILE = "barang.csv"
TRANSAKSI_FILE = "transaksi.csv"

# ======================
# INIT FILE
# ======================
if not os.path.exists(BARANG_FILE):
    df_barang = pd.DataFrame(columns=[
        "Kode Barang", "Nama Barang", "Harga Beli", "Harga Jual", "Stok"
    ])
    df_barang.to_csv(BARANG_FILE, index=False)

if not os.path.exists(TRANSAKSI_FILE):
    df_transaksi = pd.DataFrame(columns=[
        "Kode Transaksi", "Tanggal", "Jenis Transaksi", "Kode Barang", "Jumlah"
    ])
    df_transaksi.to_csv(TRANSAKSI_FILE, index=False)

# ======================
# LOAD DATA
# ======================
def load_barang():
    return pd.read_csv(BARANG_FILE)

def load_transaksi():
    return pd.read_csv(TRANSAKSI_FILE)

# ======================
# STREAMLIT UI
# ======================
st.title("📦 Sistem Manajemen Stok & Penjualan")

menu = st.sidebar.selectbox(
    "Menu",
    ["Data Barang", "Transaksi", "Laporan & Analisis"]
)

# ======================
# MENU DATA BARANG
# ======================
if menu == "Data Barang":
    st.header("📋 Manajemen Data Barang")
    df_barang = load_barang()

    with st.form("form_barang"):
        kode = st.text_input("Kode Barang")
        nama = st.text_input("Nama Barang")
        harga_beli = st.number_input("Harga Beli", min_value=0)
        harga_jual = st.number_input("Harga Jual", min_value=0)
        stok = st.number_input("Stok", min_value=0)
        submit = st.form_submit_button("Tambah Barang")

        if submit:
            if kode in df_barang["Kode Barang"].values:
                st.error("Kode barang sudah ada!")
            else:
                new_data = {
                    "Kode Barang": kode,
                    "Nama Barang": nama,
                    "Harga Beli": harga_beli,
                    "Harga Jual": harga_jual,
                    "Stok": stok
                }
                df_barang = df_barang.
