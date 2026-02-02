import streamlit as st
import pandas as pd
from datetime import datetime
import os

# =====================
# FILE PATH
# =====================
BARANG_FILE = "barang.csv"
TRANSAKSI_FILE = "transaksi.csv"

# =====================
# INIT FILE JIKA BELUM ADA
# =====================
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

# =====================
# FUNCTION LOAD DATA
# =====================
def load_barang():
    return pd.read_csv(BARANG_FILE)

def load_transaksi():
    return pd.read_csv(TRANSAKSI_FILE)

# =====================
# STREAMLIT UI
# =====================
st.title("📦 Sistem Manajemen Stok & Penjualan UMKM")

menu = st.sidebar.selectbox(
    "Menu",
    ["Data Barang", "Transaksi", "Laporan & Analisis"]
)

# =====================
# MENU DATA BARANG
# =====================
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
            if kode == "" or nama == "":
                st.error("Kode dan Nama tidak boleh kosong")
            elif kode in df_barang["Kode Barang"].values:
                st.error("Kode barang sudah ada")
            else:
                new_data = {
                    "Kode Barang": kode,
                    "Nama Barang": nama,
                    "Harga Beli": harga_beli,
                    "Harga Jual": harga_jual,
                    "Stok": stok
                }

                df_barang = df_barang._append(new_data, ignore_index=True)
                df_barang.to_csv(BARANG_FILE, index=False)
                st.success("Barang berhasil ditambahkan")

    st.subheader("📦 Daftar Barang")
    st.dataframe(df_barang)

# =====================
# MENU TRANSAKSI
# =====================
elif menu == "Transaksi":
    st.header("💰 Transaksi Penjualan & Pembelian")
    df_barang = load_barang()
    df_transaksi = load_transaksi()

    if df_barang.empty:
        st.warning("Data barang masih kosong")
    else:
        with st.form("form_transaksi"):
            kode_trx = st.text_input("Kode Transaksi")
            jenis = st.selectbox("Jenis Transaksi", ["Pembelian", "Penjualan"])
            kode_barang = st.selectbox("Kode Barang", df_barang["Kode Barang"])
            jumlah = st.number_input("Jumlah", min_value=1)
            submit_trx = st.form_submit_button("Simpan Transaksi")

            if submit_trx:
                try:
                    idx = df_barang[df_barang["Kode Barang"] == kode_barang].index[0]

                    if jenis == "Penjualan" and df_barang.loc[idx, "Stok"] < jumlah:
                        st.error("Stok tidak mencukupi")
                    else:
                        if jenis == "Penjualan":
                            df_barang.loc[idx, "Stok"] -= jumlah
                        else:
                            df_barang.loc[idx, "Stok"] += jumlah

                        transaksi = {
                            "Kode Transaksi": kode_trx,
                            "Tanggal": datetime.now().strftime("%Y-%m-%d"),
                            "Jenis Transaksi": jenis,
                            "Kode Barang": kode_barang,
                            "Jumlah": jumlah
                        }

                        df_transaksi = df_transaksi._append(transaksi, ignore_index=True)
                        df_barang.to_csv(BARANG_FILE, index=False)
                        df_transaksi.to_csv(TRANSAKSI_FILE, index=False)

                        st.success("Transaksi berhasil disimpan")
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")

    st.subheader("📑 Riwayat Transaksi")
    st.dataframe(df_transaksi)

# =====================
# MENU LAPORAN & ANALISIS
# =====================
elif menu == "Laporan & Analisis":
    st.header("📊 Laporan & Analisis")
    df_barang = load_barang()
    df_transaksi = load_transaksi()

    if df_barang.empty:
        st.warning("Belum ada data")
    else:
        df_jual = df_transaksi[df_transaksi["Jenis Transaksi"] == "Penjualan"]
        penjualan = df_jual.groupby("Kode Barang")["Jumlah"].sum()

        st.subheader("🔥 Barang Terlaris")
        if not penjualan.empty:
            st.write(penjualan.sort_values(ascending=False))
        else:
            st.info("Belum ada transaksi penjualan")

        st.subheader("⚠️ Stok Terendah")
        st.write(df_barang.sort_values("Stok").head(3))

        st.subheader("💸 Laba / Rugi")
        total_laba = 0
        for _, row in df_barang.iterrows():
            terjual = penjualan.get(row["Kode Barang"], 0)
            total_laba += terjual * (row["Harga Jual"] - row["Harga Beli"])

        st.metric("Total Laba", f"Rp {total_laba:,.0f}")
