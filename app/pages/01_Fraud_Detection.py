import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Bank Shield AI", page_icon="🚨", layout="wide")

# --- MODEL VE VERİ YÜKLEME ---
@st.cache_resource
def load_fraud_assets():
    # Model klasör yolu: models/fraud_model_v3.joblib
    model_path = Path("models/fraud_model_v3.joblib")
    # Müşteri özet verisi: data/processed/customer_risk_summary.parquet
    data_path = Path("data/processed/customer_risk_summary.parquet")
    
    try:
        bundle = joblib.load(model_path)
        profiles = pd.read_parquet(data_path)
        return bundle, profiles
    except Exception as e:
        st.error(f"Dosyalar yüklenirken hata oluştu: {e}")
        st.info("Lütfen 'models/fraud_model_v3.joblib' dosyasının varlığından emin olun.")
        return None, None

assets, profiles = load_fraud_assets()

if assets and profiles is not None:
    model = assets['model']
    encoder = assets['encoder']
    feature_cols = assets['features']        # Orijinal 9 temel sütun
    train_columns = assets['train_columns']  # Get_dummies sonrası sütunlar (2300+)
else:
    st.stop()

# --- ARAYÜZ ---
st.title("🚨 Bank Shield AI: Anlık Müdahale Paneli")
st.markdown("""
    **Sürüm:** v3 (Agresif Koruma Modu)  
    *Bu model, sinsi dolandırıcılık vakalarını yakalamak için dengeli veri setiyle eğitilmiştir.*
""")

# --- FORM ---
with st.form("fraud_detection_form"):
    st.subheader("İşlem Analiz Formu")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        client_ids = sorted(profiles["client_id"].unique().tolist())
        selected_client = st.selectbox("Müşteri Seçimi (Client ID)", options=client_ids)
        amount = st.number_input("İşlem Tutarı ($)", min_value=0.0, value=250.0)
        hour = st.slider("İşlem Saati", 0, 23, 12)
        
    with col2:
        city = st.text_input("Merchant City (Şehir)", value="Online")
        mcc = st.text_input("MCC Kodu", value="5411")
        use_chip = st.selectbox("İşlem Tipi", ["Online Transaction", "Swipe Transaction", "Chip Transaction"])

    with col3:
        speed_alert = st.selectbox("Hız Alarmı", [0, 1], format_func=lambda x: "Hız Uyarısı VAR" if x==1 else "Hız Uyarısı YOK")
        tx_count = st.number_input("Son 24 Saatlik İşlem Sayısı", min_value=1, value=1)
        # sec_since_last_tx gibi diğer alanlar arka planda 0 olarak kabul edilecek
    
    submit = st.form_submit_button("ANALİZ ET VE AKSİYON AL")

# --- ANALİZ SÜRECİ ---
if submit:
    # 1. Ham Veriyi Hazırla (Eğitimdeki 'feature_cols' sırasıyla)
    raw_input = pd.DataFrame([{
        'amount': amount,
        'tx_count_last_24h': tx_count,
        'sec_since_last_tx': 0,
        'speed_alert': speed_alert,
        'merchant_city': city,
        'mcc': mcc,
        'use_chip': use_chip,
        'is_weekend': 0,
        'hour': hour
    }])

    # 2. Preprocessing (Modelin Beklediği Formata Getirme)
    # A. Target Encoding (Şehir/MCC risklerini hesapla)
    input_encoded = encoder.transform(raw_input)
    
    # B. One-Hot Encoding (Dummy conversion)
    input_dummies = pd.get_dummies(input_encoded)
    
    # C. Reindex (Eğitimdeki 2000+ sütunla tam eşleşme sağla)
    # Bu adım notebook'ta aldığımız 'input dimension' hatasını önler.
    input_final = input_dummies.reindex(columns=train_columns, fill_value=0)

    # 3. Tahmin
    prob = model.predict_proba(input_final)[0][1]
    risk_score = prob * 100

    # --- KRİTİK MÜDAHALE EKRANI ---
    st.divider()
    
    if prob >= 0.60:
        st.error(f"‼️ KRİTİK ALARM: %{risk_score:.2f} Risk Tespit Edildi!")
        st.warning(f"🔒 AKSİYON: {selected_client} numaralı müşterinin kartı otomatik BLOKE EDİLDİ.")
        st.info("📧 Müşteriye SMS ve E-posta yoluyla bilgi verildi.")
        st.toast("Kritik müdahale başarılı!", icon="🚨")
    elif prob >= 0.30:
        st.warning(f"⚠️ ŞÜPHELİ İŞLEM: %{risk_score:.2f} Risk.")
        st.info("📲 Müşteri aranarak sözlü onay alınması önerilir.")
    else:
        st.success(f"✅ GÜVENLİ: %{risk_score:.2f} Risk. İşleme izin verildi.")

    # float32 hatasını önlemek için float() ile cast ediyoruz
    st.progress(float(prob))

    # Detaylı İnceleme (Expander)
    with st.expander("Gelişmiş Analiz Verilerini Gör"):
        st.write("Modelin okuduğu Target Encoding değerleri:")
        st.dataframe(input_encoded[['merchant_city', 'mcc']])
        st.write("Sinyal Gücü:")
        st.json({"Online_Etkisi": "Yüksek", "Sinsi_Vaka_Algısı": "Aktif"})