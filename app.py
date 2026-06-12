import streamlit as st
import pandas as pd

# Konfigurasi Halaman Light Theme Infographic
st.set_page_config(page_title="Inflasi BBM Infografis", layout="wide")

def load_data():
    return pd.read_csv('data/clean_bbm_data.csv')

def format_rupiah(angka):
    if pd.isna(angka):
        return "Rp 0"
    return f"Rp {angka:,.0f}".replace(',', '.')

df = load_data()

# ==========================================
# CUSTOM CSS STYLE (Typography & Colors)
# ==========================================
st.markdown("""
<style>
/* Inject Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Roboto:wght@400;700&display=swap');

/* Base Theme */
.stApp {
    background-color: #FDFBF7;
}

/* Typography Classes */
.main-title {
    font-family: 'Playfair Display', serif;
    color: #4A8B6A;
    font-size: 36px;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0px;
}
.sub-title {
    font-family: 'Playfair Display', serif;
    color: #333333;
    font-size: 32px;
    font-weight: 700;
    text-decoration: underline;
    text-decoration-color: #4A8B6A;
    text-decoration-thickness: 3px;
    text-underline-offset: 6px;
    margin-top: 40px;
    margin-bottom: 5px;
}
.desc-text {
    font-family: 'Roboto', sans-serif;
    color: #444444;
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 30px;
}
.year-display {
    font-family: 'Playfair Display', serif;
    color: #4A8B6A;
    font-size: 40px;
    text-align: right;
    font-weight: 900;
    margin-top: 10px;
}
.big-price-container {
    margin-top: 30px;
    display: flex;
    align-items: baseline;
}
.big-year {
    font-family: 'Playfair Display', serif;
    font-size: 36px;
    color: #4A8B6A;
    font-weight: 700;
    margin-right: 15px;
}
.big-price {
    font-family: 'Playfair Display', serif;
    color: #4A8B6A;
    font-size: 70px;
    font-weight: 900;
    line-height: 1;
}
.event-box {
    margin-top: 40px; 
    padding-left: 20px; 
    border-left: 5px solid #4A8B6A; 
    font-family: 'Roboto', sans-serif; 
    font-size: 20px; 
    color: #555;
    background-color: #f3f1eb;
    padding: 15px 20px;
    border-radius: 0px 8px 8px 0px;
}

/* Visualization CSS */
.fuel-tank-container {
    display: flex;
    align-items: flex-end;
    height: 320px;
    margin-top: 30px;
    padding-bottom: 10px;
    border-bottom: 3px solid #ddd;
}
.fuel-tank {
    background-color: #4A8B6A;
    width: 160px;
    border-radius: 12px 12px 4px 4px;
    border: 5px solid #333333;
    position: relative;
    transition: height 0.6s cubic-bezier(0.25, 0.8, 0.25, 1);
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 4px 4px 0px rgba(0,0,0,0.1);
}
.fuel-tank::before {
    content: '⛽';
    font-size: 50px;
    position: absolute;
    opacity: 0.8;
}
.fuel-tank::after {
    /* Tutup atas tangki */
    content: '';
    position: absolute;
    top: -15px;
    width: 60px;
    height: 10px;
    background-color: #333;
    border-radius: 3px;
}
.volume-text {
    font-family: 'Roboto', sans-serif;
    font-size: 40px;
    color: #333;
    font-weight: 900;
    margin-left: 40px;
    line-height: 1.1;
}
.volume-text span {
    font-size: 20px;
    font-weight: 400;
    color: #666;
}

/* Hide streamlit default top padding */
.block-container {
    padding-top: 2rem !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER SECTION
# ==========================================
col_header1, col_header2 = st.columns([2, 1])

with col_header1:
    st.markdown('<div class="main-title">INFLASI DIJELASKAN MELALUI BBM</div>', unsafe_allow_html=True)
    # Dropdown Jenis BBM
    bensin_type = st.selectbox("Analisis Berdasarkan:", ["Premium/Pertalite", "Solar", "Pertamax"], label_visibility="collapsed")

# Menentukan kolom harga berdasarkan dropdown
if bensin_type == "Premium/Pertalite":
    col_nom = 'Harga_Premium_Nominal'
    col_real = 'Harga_Premium_Real'
elif bensin_type == "Solar":
    col_nom = 'Harga_Solar_Nominal'
    col_real = 'Harga_Solar_Real'
else:
    col_nom = 'Harga_Pertamax_Nominal'
    col_real = 'Harga_Pertamax_Real'

with col_header2:
    min_year = int(df['Tahun'].min())
    max_year = int(df['Tahun'].max())
    
    # Karena Pertamax baru ada 1999, sesuaikan min_year jika perlu
    if bensin_type == "Pertamax":
        min_year = 1999
        
    selected_year = st.slider("Geser Tahun", min_value=min_year, max_value=max_year, value=max_year, label_visibility="collapsed")
    st.markdown(f'<div class="year-display">{selected_year} | Indonesia</div>', unsafe_allow_html=True)

st.markdown("<hr style='border-top: 2px solid #e0ddd3; margin-top: 0px;'>", unsafe_allow_html=True)

# Mengambil data tahun terpilih
data_selected = df[df['Tahun'] == selected_year].iloc[0]
harga_nominal = data_selected[col_nom]
harga_real = data_selected[col_real]
event = data_selected['Ringkasan_Event']

# ==========================================
# MAIN CONTENT / INFOGRAPHIC BODY
# ==========================================
col_left, col_right = st.columns(2, gap="large")

with col_left:
    st.markdown('<div class="sub-title">1. PENURUNAN NILAI UANG</div>', unsafe_allow_html=True)
    st.markdown('<div class="desc-text">Dengan pecahan uang Rp 100.000, berapa liter yang Anda dapatkan? (Geser slider!)</div>', unsafe_allow_html=True)
    
    if pd.isna(harga_nominal) or harga_nominal == 0:
        st.warning(f"{bensin_type} belum beredar di tahun {selected_year}.")
    else:
        # Kalkulasi Volume
        uang_tetap = 100000
        volume = uang_tetap / harga_nominal
        
        # Max volume history untuk rasio tinggi CSS (Contoh: max volume Premium = 100000/150 = 666 L)
        max_volume = 100000 / df[col_nom].min()
        
        # Menghitung tinggi tangki (max 300px). Menggunakan akar kuadrat (sqrt) agar penurunan drastis lebih terlihat proporsional secara area, tidak linear yang membuat tahun 2026 terlalu pipih.
        import math
        tank_height = (math.sqrt(volume) / math.sqrt(max_volume)) * 300
        
        # Batas minimum agar garis masih terlihat sedikit jika volumenya sangat kecil
        if tank_height < 15:
            tank_height = 15
            
        st.markdown(f"""
        <div class="fuel-tank-container">
            <div class="fuel-tank" style="height: {tank_height}px;"></div>
            <div class="volume-text">
                {volume:,.1f} <span style="font-size:30px;">Liter</span><br>
                <span>Sama dengan <b>{volume/4:,.0f}x</b> isi penuh tangki motor!</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="sub-title">2. KENAIKAN HARGA</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="desc-text">Harga per liter {bensin_type}</div>', unsafe_allow_html=True)
    
    if not pd.isna(harga_nominal) and harga_nominal > 0:
        st.markdown(f"""
        <div class="big-price-container">
            <div class="big-year">{selected_year} |</div>
            <div class="big-price">{format_rupiah(harga_nominal)}</div>
        </div>
        <div style="font-family: 'Roboto', sans-serif; font-size: 18px; color: #666; margin-top: 5px; margin-left: 5px;">
            (Setara dengan <b>{format_rupiah(harga_real)}</b> daya beli masa kini)
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown(f"""
    <div class="event-box">
        <strong style="color:#4A8B6A;">Konteks Sejarah {selected_year}</strong><br>
        {event}
    </div>
    """, unsafe_allow_html=True)

