
import streamlit as st
import pandas as pd
import joblib

# Load the trained model
model = joblib.load("fraud_detection_pipeline.pkl")

st.set_page_config(page_title="Fraud Detection App", page_icon="💳")
st.title("💳 Fraud Detection Prediction App")
st.markdown("Enter transaction details — balances will update automatically!")

st.divider()

# --- Input Fields ---
transaction_type = st.selectbox("Transaction Type", ["PAYMENT", "TRANSFER", "CASH_OUT", "DEPOSIT"])
amount = st.number_input("Amount", min_value=0.0, value=1000.0)
oldbalanceOrg = st.number_input("Old Balance (Sender)", min_value=0.0, value=10000.0)
oldbalanceDest = st.number_input("Old Balance (Receiver)", min_value=0.0, value=0.0)

# --- Automatically Calculate New Balances ---
newbalanceOrig = oldbalanceOrg - amount if oldbalanceOrg >= amount else 0.0
newbalanceDest = oldbalanceDest + amount

# 📍 ADD THIS BLOCK BELOW ---
manual_edit = st.checkbox("✏️ Manually edit new balances (optional)")

if manual_edit:
    newbalanceOrig = st.number_input("New Balance (Sender)", min_value=0.0, value=newbalanceOrig)
    newbalanceDest = st.number_input("New Balance (Receiver)", min_value=0.0, value=newbalanceDest)
# 📍 ------------------------

# Display current calculated or edited balances
st.info(f"""
💰 **Current Balances**
- Sender New Balance: ₹{newbalanceOrig:,.2f}  
- Receiver New Balance: ₹{newbalanceDest:,.2f}
""")

# --- Prediction Section ---
if st.button("🔍 Predict"):
    input_data = pd.DataFrame([{
        "type": transaction_type,
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest
    }])

    prediction = model.predict(input_data)[0]

    st.subheader(f"Prediction: **{'Fraudulent' if prediction == 1 else 'Legitimate'}**")

    if prediction == 1:
        st.error("⚠️ This transaction might be fraudulent!")
    else:
        st.success("✅ This transaction looks legitimate.")
