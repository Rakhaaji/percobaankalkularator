import streamlit as st

def get_sample_size(lot_size, inspection_level):
    """Menentukan ukuran sampel berdasarkan ukuran lot dan tingkat inspeksi"""
    # Tabel ukuran sampel untuk tingkat inspeksi umum dan khusus
    general_level = {
        'I': [2, 8, 20, 50, 125, 315, 800, 2000, 5000, 12500, 31500],
        'II': [2, 8, 20, 50, 125, 315, 800, 2000, 5000, 12500, 31500],
        'III': [2, 8, 20, 50, 125, 315, 800, 2000, 5000, 12500, 31500]
    }
    
    special_level = {
        'S-1': [2, 3, 5, 8, 13, 20, 32, 50, 80, 125, 200],
        'S-2': [2, 3, 5, 8, 13, 20, 32, 50, 80, 125, 200],
        'S-3': [2, 3, 5, 8, 13, 20, 32, 50, 80, 125, 200],
        'S-4': [2, 3, 5, 8, 13, 20, 32, 50, 80, 125, 200]
    }
    
    # Rentang ukuran lot
    lot_ranges = [
        (2, 8), (9, 15), (16, 25), (26, 50), (51, 90),
        (91, 150), (151, 280), (281, 500), (501, 1200),
        (1201, 3200), (3201, 10000), (10001, 35000),
        (35001, 150000), (150001, 500000), (500001, float('inf'))
    ]
    
    # Cari indeks yang sesuai berdasarkan ukuran lot
    index = 0
    for i, (low, high) in enumerate(lot_ranges):
        if low <= lot_size <= high:
            index = i
            break
    
    # Dapatkan ukuran sampel berdasarkan tingkat inspeksi
    if inspection_level in ['I', 'II', 'III']:
        return general_level[inspection_level][min(index, len(general_level[inspection_level])-1)]
    elif inspection_level in ['S-1', 'S-2', 'S-3', 'S-4']:
        return special_level[inspection_level][min(index, len(special_level[inspection_level])-1)]
    else:
        return 0  # Tingkat inspeksi tidak valid

def aql_calculator(lot_size, inspection_level, aql_level):
    """Menghitung nilai AQL dengan dukungan GIL"""
    # Batas AQL standar (terima, tolak)
    aql_limits = {
        0.010: (0, 1),
        0.015: (0, 1),
        0.025: (0, 1),
        0.040: (0, 1),
        0.065: (0, 1),
        0.10: (0, 1),
        0.15: (0, 1),
        0.25: (0, 2),
        0.40: (0, 3),
        0.65: (0, 4),
        1.0: (0, 7),
        1.5: (0, 10),
        2.5: (0, 14),
        4.0: (0, 20),
        6.5: (0, 30)
    }
    
    # Dapatkan ukuran sampel berdasarkan tingkat inspeksi
    sample_size = get_sample_size(lot_size, inspection_level)
    
    if sample_size == 0:
        return {"Error": "Tingkat inspeksi tidak valid"}
    
    # Hitung titik terima dan tolak
    if aql_level in aql_limits:
        accept_point, reject_point = aql_limits[aql_level]
        
        # Penanganan khusus untuk level AQL yang sangat kecil
        if aql_level <= 0.065:
            if sample_size <= 8:
                accept_point = 0
                reject_point = 1
            elif sample_size <= 32:
                accept_point = 1 if aql_level >= 0.065 else 0
                reject_point = 2 if aql_level >= 0.065 else 1
            else:
                accept_point = int(sample_size * (aql_level / 100)) if (sample_size * (aql_level / 100)) >= 1 else 0
                reject_point = accept_point + 1
        else:
            accept_point = int(sample_size * (aql_level / 100))
            reject_point = accept_point + 1
    else:
        return {"Error": "Level AQL tidak valid"}
    
    return {
        "Sample Size": sample_size,
        "Accept Point": accept_point,
        "Reject Point": reject_point,
        "Inspection Level": inspection_level
    }

# Antarmuka Streamlit
def main():
    st.title("Kalkulator AQL dengan GIL (Tingkat Inspeksi Umum/Khusus)")
    
    st.markdown("""
    Kalkulator ini membantu menentukan ukuran sampel dan kriteria penerimaan berdasarkan:
    - Ukuran lot
    - Tingkat inspeksi (Umum I, II, III atau Khusus S-1 sampai S-4)
    - AQL (Tingkat Kualitas yang Dapat Diterima)
    """)
    
    # Input fields
    col1, col2, col3 = st.columns(3)
    
    with col1:
        lot_size = st.number_input("Ukuran Lot", min_value=2, value=2000)
    
    with col2:
        inspection_level = st.selectbox(
            "Tingkat Inspeksi",
            options=['I', 'II', 'III', 'S-1', 'S-2', 'S-3', 'S-4'],
            index=1
        )
    
    with col3:
        aql_level = st.selectbox(
            "Level AQL (%)",
            options=[0.010, 0.015, 0.025, 0.040, 0.065, 0.10, 0.15, 0.25, 
                     0.40, 0.65, 1.0, 1.5, 2.5, 4.0, 6.5],
            index=11
        )
    
    # Tombol hitung
    if st.button("Hitung AQL"):
        result = aql_calculator(lot_size, inspection_level, aql_level)
        
        if "Error" in result:
            st.error(result["Error"])
        else:
            st.success("Hasil Perhitungan AQL")
            st.markdown(f"""
            - *Ukuran Sampel*: {result['Sample Size']}
            - *Titik Terima*: {result['Accept Point']}
            - *Titik Tolak*: {result['Reject Point']}
            - *Tingkat Inspeksi*: {result['Inspection Level']}
            """)
            
            # Penjelasan tambahan
            st.info(f"""
            Untuk ukuran lot {lot_size} dengan tingkat inspeksi {inspection_level} dan AQL {aql_level}%:
            - Anda harus memeriksa *{result['Sample Size']}* item
            - Terima lot jika cacat *≤ {result['Accept Point']}*
            - Tolak lot jika cacat *≥ {result['Reject Point']}*
            """)

if _name_ == "_main_":
    main()
