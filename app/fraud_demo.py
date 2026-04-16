import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(page_title="Fraud MVP", layout="wide")

st.title("Fraud Detection MVP")
st.write("Transaction risk prediction demo")

# MODEL PATH (SENİN PROJEYE GÖRE)
model = joblib.load("models/fraud_mvp_model.joblib")

# INPUT ALANI
st.subheader("Transaction Inputs")

col1, col2 = st.columns(2)

with col1:
    amount = st.number_input("Amount", value=50.0)
    use_chip = st.selectbox("Transaction Type", [
        "Swipe Transaction", "Chip Transaction", "Online Transaction"
    ])
    merchant_city = st.text_input("Merchant City", "New York")
    merchant_state = st.text_input("Merchant State", "NY")
    mcc = st.text_input("MCC", "5411")
    is_return = st.selectbox("Is Return?", [0, 1])

with col2:
    current_age = st.number_input("Age", value=30)
    gender = st.selectbox("Gender", ["Male", "Female"])
    yearly_income = st.number_input("Yearly Income", value=50000.0)
    credit_score = st.number_input("Credit Score", value=650)
    hour = st.slider("Hour", 0, 23, 12)
    day = st.slider("Day", 1, 31, 15)
    month = st.slider("Month", 1, 12, 6)
    year = st.slider("Year", 2010, 2025, 2019)
    per_capita_income = st.number_input("Per Capita Income", value=25000.0)
    total_debt = st.number_input("Total Debt", value=10000.0)

day_of_week = st.selectbox(
    "Day of Week",
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
)

# BUTTON
if st.button("Predict Fraud"):

    day_map = {
        "Monday":0,"Tuesday":1,"Wednesday":2,
        "Thursday":3,"Friday":4,"Saturday":5,"Sunday":6
    }

    # FEATURE ENGINEERING (DEMO VERSION)
    log_amount = np.log1p(amount)
    amount_zscore = 0
    high_amount = int(amount > 100)
    amount_to_limit_ratio = 0.01

    is_online = int("online" in use_chip.lower())
    is_chip_used = int("chip" in use_chip.lower())
    is_swipe = int("swipe" in use_chip.lower())

    is_weekend = int(day_of_week in ["Saturday","Sunday"])
    is_night = int(hour < 6 or hour > 22)
    is_peak_hour = int(hour in [12,13,18,19,20])

    # MOCK BEHAVIOR (MVP DEMO)
    user_tx_count = 10
    user_mean_amount = 60
    user_std_amount = 20
    amount_deviation = amount - user_mean_amount
    time_diff = 300
    fast_tx = int(time_diff < 60)
    very_fast_tx = int(time_diff < 10)

    rolling_mean_3 = 55
    rolling_std_3 = 15
    rolling_amount_deviation = amount - rolling_mean_3

    merchant_risk_flag = 0

    # DATAFRAME
    df_input = pd.DataFrame([{
        "amount": amount,
        "per_capita_income": per_capita_income,
        "total_debt": total_debt,
        "log_amount": log_amount,
        "amount_zscore": amount_zscore,
        "high_amount": high_amount,
        "amount_to_limit_ratio": amount_to_limit_ratio,
        "hour": hour,
        "day": day,
        "month": month,
        "year": year,
        "day_of_week": day_of_week,
        "day_of_week_num": day_map[day_of_week],
        "is_weekend": is_weekend,
        "is_night": is_night,
        "is_peak_hour": is_peak_hour,
        "use_chip": use_chip,
        "is_online": is_online,
        "is_chip_used": is_chip_used,
        "is_swipe": is_swipe,
        "merchant_city": merchant_city,
        "merchant_state": merchant_state,
        "mcc": mcc,
        "merchant_risk_flag": merchant_risk_flag,
        "is_return": is_return,
        "current_age": current_age,
        "gender": gender,
        "yearly_income": yearly_income,
        "credit_score": credit_score,
        "user_tx_count": user_tx_count,
        "user_mean_amount": user_mean_amount,
        "user_std_amount": user_std_amount,
        "amount_deviation": amount_deviation,
        "time_diff": time_diff,
        "fast_tx": fast_tx,
        "very_fast_tx": very_fast_tx,
        "rolling_mean_3": rolling_mean_3,
        "rolling_std_3": rolling_std_3,
        "rolling_amount_deviation": rolling_amount_deviation
    }])

    # MODEL
    pred = model.predict(df_input)[0]
    proba = model.predict_proba(df_input)[0,1]

    st.subheader("Result")
    st.metric("Fraud Probability", f"{proba:.2%}")
    st.metric("Risk Score", round(proba*100,2))

    if proba > 0.8:
        st.error("High Risk 🚨")
    elif proba > 0.5:
        st.warning("Medium Risk ⚠️")
    else:
        st.success("Low Risk ✅")

    st.write("Prediction:", "Fraud" if pred==1 else "Not Fraud")