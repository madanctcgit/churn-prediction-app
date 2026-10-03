import streamlit as st
import requests
import numpy as np
import pandas as pd
import os
import streamlit as st
import requests

st.title("SuperKart Sales Prediction")

# Collect input fields from user
product_id = st.text_input("Product Id", "FD6114")
product_weight = st.number_input("Product Weight", value=1.0)
product_sugar_content = st.selectbox("Product Sugar Content", ["Regular", "Low Sugar", "No Sugar"])
product_allocated_area = st.number_input("Product Allocated Area", value=0.0)
product_type = st.selectbox(
    "Product Type",
    [
        "Meat", "Snack Foods", "Hard Drinks", "Dairy", "Canned", "Soft Drinks",
        "Health and Hygiene", "Baking Goods", "Bread", "Breakfast", "Frozen Foods",
        "Fruits and Vegetables", "Household", "Seafood", "Starchy Foods", "Others"
    ]
)
product_mrp = st.number_input("Product MRP", value=45.0)
store_id = st.text_input("Store Id", "S001")
store_est_year = st.number_input("Store Establishment Year", value=2005)
store_size = st.selectbox("Store Size", ["Low", "Medium", "High"])
store_location_city_type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
store_type = st.selectbox("Store Type", ["Departmental Store", "Supermarket Type 1", "Supermarket Type 2", "Food Mart"])

# When user clicks Predict
if st.button("Predict Sales"):
    # Build JSON payload
    payload = {
        "features": {
            "Product_Id": product_id,
            "Product_Weight": product_weight,
            "Product_Sugar_Content": product_sugar_content,
            "Product_Allocated_Area": product_allocated_area,
            "Product_Type": product_type,
            "Product_MRP": product_mrp,
            "Store_Id": store_id,
            "Store_Establishment_Year": store_est_year,
            "Store_Size": store_size,
            "Store_Location_City_Type": store_location_city_type,
            "Store_Type": store_type
        }
    }

    try:
        # Call backend API
        response = requests.post("https://super-duper-halibut-gxrj5xjxvjq625xj.github.dev/v1/predict", json=payload)
        if response.status_code == 200:
            result = response.json()
            st.success(f"Predicted Sales: {result['prediction']}")
        else:
            st.error(f"Backend error: {response.text}")
    except Exception as e:
        st.error(f"Could not connect to backend: {e}")

# --- Batch Prediction ---

# Always show the button
if st.button("Predict Batch Sales"):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Preview of uploaded data:", df.head())

        records = df.to_dict(orient="records")
        payload = {"features": records}
        print(payload);
        try:
            response = requests.post("http://localhost:7860/v1/predictbatch", json=payload)
            if response.status_code == 200:
                result = response.json()
                st.success("Batch Predictions:")
                st.write(result["predictions"])
            else:
                st.error(f"Backend error: {response.text}")
        except Exception as e:
            st.error(f"Could not connect to backend: {e}")
    else:
        st.warning("Please upload a CSV file first.")
