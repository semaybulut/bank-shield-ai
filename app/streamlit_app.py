import streamlit as st
import base64
from pathlib import Path

# --- LOGO OKUMA FONKSİYONU ---
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        return None

# logo.png dosyanın yolunu belirle
# Dosya streamlit_app.py ile aynı klasördeyse "./logo.png"
# Eğer bir üst klasördeyse "../logo.png" denemelisin
current_dir = Path(__file__).parent
logo_path = current_dir / "logo.png"
logo_base64 = get_base64_image(str(logo_path))

# --- HEADER GÜNCELLEME ---
if logo_base64:
    logo_html = f'<img src="data:image/png;base64,{logo_base64}" width="200">'
else:
    # Logo bulunamazsa yedek olarak yazı gösterir
    logo_html = '<h2 style="color: #004587; margin:0;">CaixaBank</h2>'

st.markdown(f"""
    <div class="header-box">
        {logo_html}
        <div style="color: #004587; font-weight: bold;">Kişisel Bankacılık | Kurumsal | AI Risk Portal</div>
    </div>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="CaixaBank AI Risk Hub", page_icon="🏦", layout="wide")

# --- GELİŞMİŞ CSS: GERÇEK BANKACILIK TEMASI ---
st.markdown("""
    <style>
    /* Header düzeni: Logo sol, Butonlar sağ */
    .header-box {
        background-color: white;
        padding: 15px 50px;
        display: flex;
        justify-content: space-between; /* Bu satır butonları sağa iter */
        align-items: center;
        border-bottom: 3px solid #ff6600;
    }

    .header-right-menu {
        display: flex;
        gap: 15px;
    }
    
    /* Müşteri Ol Butonu (Kırmızı) */
    .btn-register {
        background-color: #eb0000;
        color: white !important;
        padding: 10px 25px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
        transition: 0.3s;
    }
    
    /* Giriş Yap Butonu (Yeşil) */
    .btn-login {
        background-color: #00a550;
        color: white !important;
        padding: 10px 25px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
        transition: 0.3s;
    }

    .btn-register:hover, .btn-login:hover {
        opacity: 0.8;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)


# --- HERO SECTION ---
# --- HEADER GÜNCELLEMESİ ---
st.markdown(f"""
    <div class="header-box">
        <div style="display: flex; align-items: center;">
            {logo_html}
        </div>
        <div class="header-right-menu">
            <a href="#" class="btn-register">Müşteri Ol</a>
            <a href="#" class="btn-login">Giriş Yap</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- SERVİS KARTLARI ---
st.markdown('<div style="padding: 0 50px;">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("""
        <div class="service-card">
            <h2 style="color: #004587;">🔍 Fraud Detection</h2>
            <p style="color: #666;">Şüpheli işlemlerinizi anlık olarak XGBoost motorumuzla analiz edin ve sahteciliği saniyeler içinde durdurun.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Hemen Analiz Et ➔", key="btn_fraud"):
        st.switch_page("pages/01_Fraud_Detection.py")

with col2:
    st.markdown("""
        <div class="service-card">
            <h2 style="color: #004587;">📊 Behavioral Risk</h2>
            <p style="color: #666;">Müşteri davranışlarını ve geçmiş verileri inceleyerek uzun vadeli risk skorlarını görüntüleyin.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Skorları Görüntüle ➔", key="btn_risk"):
        st.switch_page("pages/02_Behavioral_Risk.py")

with col3:
    st.markdown("""
        <div class="service-card">
            <h2 style="color: #004587;">🛡️ Security Logs</h2>
            <p style="color: #666;">Sistem üzerindeki geçmiş alarmları ve müdahale raporlarını detaylı olarak inceleyin.</p>
        </div>
    """, unsafe_allow_html=True)
    st.button("Raporlar (Yakında)", disabled=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- ALT BİLGİ (FOOTER) ---
st.markdown("""
    <div style="text-align: center; margin-top: 100px; padding: 20px; color: #999; font-size: 0.8rem;">
        © 2026 CaixaBank AI Risk Management Solutions. All Rights Reserved.
    </div>
    """, unsafe_allow_html=True)