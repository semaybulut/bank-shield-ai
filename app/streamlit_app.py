import streamlit as st
import base64
from pathlib import Path

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="CaixaBank AI Risk Hub", page_icon="🏦", layout="wide")

# --- LOGO OKUMA ---
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        return None

current_dir = Path(__file__).parent
logo_path = current_dir / "logo.png"
logo_base64 = get_base64_image(str(logo_path))

if logo_base64:
    logo_html = f'<img src="data:image/png;base64,{logo_base64}" width="200">'
else:
    logo_html = '<h2 style="color: #004587; margin:0;">CaixaBank</h2>'

# --- GELİŞMİŞ CSS (TEMİZLİK VE DÜZEN) ---
st.markdown("""
    <style>
    /* Genel Arkaplan */
    .main { background-color: #f0f2f5; }
    
    /* Header Alanı */
    .header-box {
        background-color: white;
        padding: 10px 50px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 3px solid #ff6600;
    }
    
    .nav-links {
        color: #004587;
        font-size: 13px;
        font-weight: 500;
        margin-bottom: 5px;
    }

    .header-right-container {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
    }

    .header-right-menu {
        display: flex;
        gap: 15px;
    }
    
    /* Butonlar */
    .btn-register {
        background-color: #eb0000;
        color: white !important;
        padding: 8px 20px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
        font-size: 14px;
    }
    
    .btn-login {
        background-color: #00a550;
        color: white !important;
        padding: 8px 20px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
        font-size: 14px;
    }

    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #004587 0%, #002e5a 100%);
        color: white;
        padding: 60px 50px;
        border-radius: 0 0 50px 50px;
        margin-bottom: 40px;
    }
    
    /* Servis Kartları */
    .service-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        height: 250px;
        border: 1px solid #e1e4e8;
    }
    
    /* Streamlit'in kendi butonlarını özelleştirme */
    div.stButton > button {
        background-color: #004587;
        color: white;
        border-radius: 50px;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER (LOGO + NAV + BUTONLAR) ---
st.markdown(f"""
    <div class="header-box">
        <div>{logo_html}</div>
        <div class="header-right-container">
            <div class="nav-links">
                Bireysel &nbsp; | &nbsp; Kurumsal &nbsp; | &nbsp; 
                <span style="font-weight: bold; color: #ff6600;">AI Risk Portal</span>
            </div>
            <div class="header-right-menu">
                <a href="#" class="btn-register">Müşteri Ol</a>
                <a href="#" class="btn-login">Giriş Yap</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown("""
    <div class="hero-section">
        <h1 style="color: white; margin-bottom: 10px;">Güvenliğiniz, Bizim Önceliğimiz.</h1>
        <p style="opacity: 0.9;">Yapay zeka destekli Risk Yönetim Portalı ile tüm işlemlerinizi 7/24 kontrol altında tutun.</p>
    </div>
    """, unsafe_allow_html=True)

# --- İÇERİK KARTLARI ---
st.markdown('<div style="padding: 0 50px;">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown('<div class="service-card"><h3>🔍 Fraud Detection</h3><p>Anlık işlem bazlı sahtecilik analizi.</p></div>', unsafe_allow_html=True)
    if st.button("Hemen Analiz Et ➔", key="f"): st.switch_page("pages/01_Fraud_Detection.py")

with c2:
    st.markdown('<div class="service-card"><h3>📊 Behavioral Risk</h3><p>Müşteri davranışsal profil analizi.</p></div>', unsafe_allow_html=True)
    if st.button("Skorları Görüntüle ➔", key="r"): st.switch_page("pages/02_Behavioral_Risk.py")

with c3:
    st.markdown('<div class="service-card"><h3>🛡️ Security Logs</h3><p>Sistem raporları ve geçmiş kayıtlar.</p></div>', unsafe_allow_html=True)
    st.button("Yakında", disabled=True)

st.markdown('</div>', unsafe_allow_html=True)
# --- ALT BİLGİ (FOOTER) ---
st.markdown("""
    <div style="text-align: center; margin-top: 80px; padding: 30px; color: #7f8c8d; font-size: 0.85rem; border-top: 1px solid #e1e4e8;">
        © 2026 CaixaBank AI Risk Management Solutions. All Rights Reserved. <br>
        <span style="font-size: 0.75rem; opacity: 0.8;">Güvenliğiniz için tüm işlemler uçtan uca şifrelenmektedir.</span>
    </div>
    """, unsafe_allow_html=True)