import streamlit as st
import math

st.set_page_config(page_title="AQL Checker", layout="centered")

# Sidebar navigation
st.sidebar.title("Menu")
page = st.sidebar.radio("Pilih Halaman", ["Beranda", "Kalkulator AQL"])

def hitung_acceptance(sample_size, aql_percent):     
    aql = aql_percent / 100
    return math.floor(sample_size * aql + 0.5)

def get_code_letter(lot_size, inspection_level):
    if lot_size <= 50:
        code_map = {"GI": "A", "GII": "B", "GIII": "C"}
    elif lot_size <= 90:
        code_map = {"GI": "B", "GII": "C", "GIII": "D"}
    elif lot_size <= 150:
        code_map = {"GI": "C", "GII": "D", "GIII": "E"}
    elif lot_size <= 280:
        code_map = {"GI": "D", "GII": "E", "GIII": "F"}
    elif lot_size <= 500:
        code_map = {"GI": "E", "GII": "F", "GIII": "G"}
    elif lot_size <= 1200:
        code_map = {"GI": "F", "GII": "G", "GIII": "H"}
    elif lot_size <= 3200:
        code_map = {"GI": "G", "GII": "H", "GIII": "J"}
    elif lot_size <= 10000:
        code_map = {"GI": "H", "GII": "J", "GIII": "K"}
    elif lot_size <= 35000:
        code_map = {"GI": "J", "GII": "K", "GIII": "L"}
    elif lot_size <= 150000:
        code_map = {"GI": "K", "GII": "L", "GIII": "M"}
    elif lot_size <= 500000:
        code_map = {"GI": "L", "GII": "M", "GIII": "N"}
    else:
        code_map = {"GI": "M", "GII": "N", "GIII": "P"}
    return code_map.get(inspection_level, "C")

def get_sample_size(code_letter):
    sample_size_table = {
        "A": 2, "B": 5, "C": 8, "D": 13, "E": 20, "F": 32,
        "G": 50, "H": 80, "J": 125, "K": 200, "L": 315,
        "M": 500, "N": 800, "P": 1250
    }
    return sample_size_table.get(code_letter, 0)

# ------------------------
# Halaman BERANDA
# ------------------------
if page == "Beranda":

    # Gaya industri dan latar belakang
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)),
                    url('https://img.freepik.com/free-vector/factory-scene-with-river-foreground_1308-32357.jpg?t=st=1746794892~exp=1746798492~hmac=316f122289c03f1f42fb412ed82a50e1399b075c6add2252da4dcd74d0668dab&w=1380');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        color: orange !important;
    }
    .container {
        background-color: rgba(0, 0, 0, 0.6);
        padding: 2rem;
        border-radius: 12px;
    }
    .feature-box {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        border: 1px solid #cbd5e0;
    }
    .group-box {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='container'>", unsafe_allow_html=True)
    st.title("🏭 Selamat Datang di Kalkulator AQL untuk Industri 4.0")

    st.markdown("""
    <h4>🔍 Apa itu AQL?</h4>
    <p><strong>AQL (Acceptable Quality Limit)</strong> adalah metode penentuan batas cacat maksimum dalam inspeksi produk.</p>
    <p>Kalkulator ini membantu memastikan bahwa produk Anda memenuhi standar kualitas industri secara efisien dan akurat. Selain itu, dengan kalkulator ini Anda dapat melakukan pekerjaan secara cepat dan lebih efisien.</p>
    """, unsafe_allow_html=True)

    st.subheader("🔧 Fitur Utama")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='feature-box'>
        ✔ Hitung Acceptance/Rejection dengan cepat<br>
        ✔ Efisien tanpa tabel AQL manual
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='feature-box'>
        📦 Dukungan berbagai ukuran lot<br>
        🏭 Cocok untuk lingkungan pabrik
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.success("👈 Gunakan menu di sebelah kiri untuk memulai kalkulasi AQL.")
    
    st.markdown("### 👩🏻‍🔬👨🏻‍🔬 Kelompok Pengembang")
    st.markdown("""
    <div class='group-box'>
    <ul>
        <li>👩🏻‍🔬 Arya Suhada Maridha</li>
        <li>👩🏻‍🔬 Aura Fathanza</li>
        <li>👩🏻‍🔬 Maulidia Aliya R</li>
        <li>👨🏻‍🔬 Rakha Wahyu Hendriaji</li>
        <li>👩🏻‍🔬 Salfa Nabigha Aureliza</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------
# Halaman KALKULATOR
# ------------------------
elif page == "Kalkulator AQL":
    st.title("⚖️ Kalkulator AQL")

    # Input
    lot_size = st.number_input("Ukuran Lot", min_value=1, value=500)
    inspection_level = st.selectbox(
        "Pilih General Inspection Level",
        options=["GI", "GII", "GIII"],
        index=1  # GII sebagai default
    )
    code_letter = get_code_letter(lot_size, inspection_level)
    sample_size = get_sample_size(code_letter)
    st.markdown(f"*Kode Huruf:* {code_letter}")
    st.markdown(f"*Ukuran Sampel:* {sample_size}")

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
        else:
            st.error("❌ LOT DITOLAK") 
            st.markdown(f"""
            Jumlah cacat yang ditemukan ({defects_found}) *melebihi* nilai batas maksimum (Ac = {acceptance_number}),
            sehingga *lot ini tidak memenuhi syarat* dan harus ditolak atau diperiksa ulang.
            """)
