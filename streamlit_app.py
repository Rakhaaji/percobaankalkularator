import streamlit as st
import math
import json
import requests
from streamlit_lottie import st_lottie

st.set_page_config(page_title="AQL Checker", layout="centered")

# Fungsi untuk menghitung Acceptance Number
def hitung_acceptance(sample_size, aql_percent):
    aql = aql_percent / 100
    return math.floor(sample_size * aql + 0.5)

# Fungsi untuk memuat animasi Lottie dari URL
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Sidebar navigation
st.sidebar.title("Menu")
page = st.sidebar.radio("Pilih Halaman", ["Beranda", "Kalkulator AQL"])

# ------------------------
# Halaman BERANDA
# ------------------------
if page == "Beranda":
    st.title("🏭 Selamat Datang di Kalkulator AQL untuk Industri 4.0")
    st.markdown("""
    <h4>🔍 Apa itu AQL?</h4>
    <p><strong>AQL (Acceptable Quality Limit)</strong> adalah metode penentuan batas cacat maksimum dalam inspeksi produk.</p>
    <p>Kalkulator ini membantu memastikan bahwa produk Anda memenuhi standar kualitas industri secara efisien dan akurat.</p>
    """, unsafe_allow_html=True)

    st.subheader("🔧 Fitur Utama")
    st.markdown("""
    - ✔ Hitung Acceptance/Rejection dengan cepat
    - 📦 Dukungan berbagai ukuran lot
    - 🏭 Cocok untuk lingkungan pabrik
    """)
    st.success("👈 Gunakan menu di sebelah kiri untuk memulai kalkulasi AQL.")
    st.markdown("### 👩🏻‍🔬👨🏻‍🔬 Kelompok Pengembang")
    st.markdown("""
    - 👩🏻‍🔬 Arya Suhada Maridha
    - 👩🏻‍🔬 Aura Fathanza
    - 👩🏻‍🔬 Maulidia Aliya R
    - 👨🏻‍🔬 Rakha Wahyu Hendriaji
    - 👩🏻‍🔬 Salfa Nabigha Aureliza
    """)

# ------------------------
# Halaman KALKULATOR
# ------------------------
elif page == "Kalkulator AQL":
    st.title("⚖ Kalkulator AQL")

    # Pilihan jenis inspeksi
    inspection_type = st.selectbox("Pilih Jenis Inspeksi", ["Normal Inspection", "General Inspection"])

    # Input
    lot_size = st.number_input("Ukuran Lot", min_value=1, value=500)
    sample_size = st.number_input("Ukuran Sampel", min_value=1, value=50)
    aql = st.number_input("Nilai AQL (%)", min_value=0.01, value=1.0, format="%.2f")
    defects_found = st.number_input("Jumlah Cacat yang Ditemukan", min_value=0, value=0)

    if st.button("Hitung Hasil"):
        acceptance_number = hitung_acceptance(sample_size, aql)
        rejection_number = acceptance_number + 1

        st.markdown(f"*Acceptance Number (Ac):* {acceptance_number}")
        st.markdown(f"*Rejection Number (Re):* {rejection_number}")
        st.markdown("### 🧾 Kesimpulan")

        if defects_found <= acceptance_number:
            st.success("✅ LOT DITERIMA")
            st.markdown(f"""
            Jumlah cacat yang ditemukan ({defects_found}) masih berada di bawah atau sama dengan nilai batas maksimum (Ac = {acceptance_number}),
            sehingga *lot ini dapat diterima* sesuai standar AQL {aql:.2f}%.
            """)
            st.balloons()  # Efek balon sebagai perayaan

            # Menampilkan animasi Lottie
            lottie_url = "https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json"  # Ganti dengan URL animasi Lottie pilihan Anda
            lottie_json = load_lottieurl(lottie_url)
            if lottie_json:
                st_lottie(lottie_json, height=300, key="success")

        else:
            st.error("❌ LOT DITOLAK")
            st.markdown(f"""
            Jumlah cacat yang ditemukan ({defects_found}) *melebihi* nilai batas maksimum (Ac = {acceptance_number}),
            sehingga *lot ini tidak memenuhi syarat* dan harus ditolak atau diperiksa ulang.
            """)
