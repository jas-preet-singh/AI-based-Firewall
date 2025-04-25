from flask import Flask, request, jsonify
import joblib
import numpy as np


model = joblib.load("random_forest_model.pkl")
scaler = joblib.load("scaler.pkl")

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        features = np.array([[data["packet_size"], data["request_frequency"], data["port"]]])
        scaled_features = scaler.transform(features)
        prediction = model.predict(scaled_features)[0]
        result = "Anomalous" if prediction == 1 else "Normal"
        return jsonify({"prediction": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
