from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
import os
# Initialize Flask app
#app = Flask(__name__)
app = Flask(__name__)

# Load serialized model
model = joblib.load("superkart_model.joblib")




# Define a route for the home page
@app.route("/")
def home():
    return "Welcome to the SuperKart System"

# Define an endpoint to predict sales for a single product
#@app.post('/v1/predict')
@app.route("/v1/predict", methods=["POST"])
def predict_sales():
    # Get JSON data from the request
    data = request.get_json()
    print(model.feature_names_in_)

    print(data);
    # Convert the extracted data into a DataFrame
    #input_data = pd.DataFrame(data["features"])
    #input_data = pd.DataFrame([data["features"]])
    input_data = pd.DataFrame([data.get("features", data)])

    # input_data = pd.DataFrame([data], columns=[
    #     "Product_Id", "Store_Id", "Product_MRP", "Product_Type", "Product_Id_char",
    #     "Product_Allocated_Area", "Store_Type", "Product_Weight","Store_Age_Years",
    #     "Store_Size", "Store_Establishment_Year", "Store_Location_City_Type",
    #     "Product_Sugar_Content","Product_Type_Category"
    # ])

    # Make a prediction using the trained model
    #prediction = model.predict(input_data).tolist()[0]
    prediction = model.predict(input_data)[0]
    # Return the prediction as a JSON response
    return jsonify({"prediction": prediction})

# Define an endpoint to predict sales for a batch of products
#@app.post('/v1/predictbatch')
@app.route("/v1/predictbatch", methods=["POST"])
def predict_sales_batch():
    file = request.files['file']
    input_data = pd.read_csv(file)

    # Ensure all required columns exist
    required = list(model.feature_names_in_)
    for col in required:
        if col not in input_data.columns:
            # Add missing column with safe default
            if col in ["Store_Establishment_Year", "Product_MRP", "Product_Weight", "Product_Allocated_Area"]:
                input_data[col] = 0   # numeric default
            else:
                input_data[col] = "Unknown"   # categorical default

    # Fill blanks with safe defaults
    for col in input_data.columns:
        if pd.api.types.is_numeric_dtype(input_data[col]):
            input_data[col] = input_data[col].fillna(0)
        else:
            input_data[col] = input_data[col].fillna("Unknown")

    # Verify schema
    missing = [col for col in required if col not in input_data.columns]
    if missing:
        return jsonify({"error": f"Still missing columns: {missing}"}), 400

    # Make predictions safely
    try:
        predictions = model.predict(input_data).tolist()
        output_dict = {str(i): round(pred, 2) for i, pred in enumerate(predictions)}
        return jsonify(output_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run the Flask app in debug mode
# if __name__ == '__main__':
#     superkart_api.run(debug=True)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860, debug=False)


# @app.route("/predict", methods=["POST"])
# def predict():
#     """
#     Expects JSON input with feature values.
#     Example:
#     {
#         "features": {
#             "Store_ID": 101,
#             "Product_Category": "Electronics",
#             "Quantity": 5,
#             ...
#         }
#     }
#     """
#     data = request.get_json(force=True)
#     features = pd.DataFrame([data["features"]])  # convert dict → DataFrame
#     prediction = model.predict(features)[0]
#     return jsonify({"prediction": prediction})



