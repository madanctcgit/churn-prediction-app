from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
import os
# Initialize Flask app
#app = Flask(__name__)
superkart_api = Flask("SuperKart")

# Load serialized model
model = joblib.load("superkart_model.joblib")




# Define a route for the home page
@superkart_api.get('/')
def home():
    return "Welcome to the SuperKart System"

# Define an endpoint to predict sales for a single product
@superkart_api.post('/v1/predict')
def predict_sales():
    # Get JSON data from the request
    data = request.get_json()
    print(data);
    # Convert the extracted data into a DataFrame
    #input_data = pd.DataFrame(data["features"])
    input_data = pd.DataFrame([data["features"]])
    # Make a prediction using the trained model
    #prediction = model.predict(input_data).tolist()[0]
    prediction = model.predict(input_data)[0]
    # Return the prediction as a JSON response
    return jsonify({"prediction": prediction})

# Define an endpoint to predict sales for a batch of products
@superkart_api.post('/v1/predictbatch')
def predict_sales_batch():
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the file into a DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for the batch data
    predictions = model.predict(input_data).tolist()

    # Create an output dictionary mapping row index to predicted sales
    output_dict = {str(i): round(pred, 2) for i, pred in enumerate(predictions)}

    return output_dict


# Run the Flask app in debug mode
# if __name__ == '__main__':
#     superkart_api.run(debug=True)
if __name__ == "__main__":
    superkart_api.run(host="0.0.0.0", port=7860, debug=False)


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

