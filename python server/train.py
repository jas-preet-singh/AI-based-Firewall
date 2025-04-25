import pandas as pd
import random
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
from sklearn.ensemble import RandomForestClassifier
csv_path = "network_logs.csv"

df = pd.read_csv(csv_path)

features = ["packet_size", "request_frequency", "port"]
X = df[features]


scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, df["anomaly_label"], test_size=0.2, random_state=42)


rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)


y_pred = rf_model.predict(X_test)


rf_accuracy = accuracy_score(y_test, y_pred)
rf_report = classification_report(y_test, y_pred)

# print(rf_accuracy)
# print(rf_report)

import joblib


model_path = "random_forest_model.pkl"
joblib.dump(rf_model, model_path)


scaler_path = "scaler.pkl"
joblib.dump(scaler, scaler_path)

model_path, scaler_path