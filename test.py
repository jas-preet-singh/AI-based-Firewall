# Step 1: Install Required Libraries


# Step 2: Import Libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Step 3: Load the Dataset
# Replace the file path with the location of your CSV file
df = pd.read_csv("small.csv")

# Inspect the first few rows of the dataset
print(df.head())

# Step 4: Handle Missing Values
# Check for missing values in the dataset
print(df.isnull().sum())

# Drop rows with missing values (or fill them with a strategy like df.fillna())
df = df.dropna()  # Alternatively, use df.fillna() if you want to fill the missing values

# Step 5: Encode Categorical Features
# Encode the categorical 'Attack Type' column
label_encoder = LabelEncoder()
df['Attack Type'] = label_encoder.fit_transform(df['Attack Type'])

# Step 6: Feature Scaling
# Standardize the numeric columns (scaling features)
scaler = StandardScaler()

# Select numeric columns to scale
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns

# Apply scaling to numeric columns
df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

# Step 7: Split Data into Features and Target
# X (features) and y (target)
X = df.drop('Attack Type', axis=1)  # All columns except 'Attack Type'
y = df['Attack Type']  # 'Attack Type' is the target variable

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 8: Train the Model
# Create a Random Forest Classifier model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model with the training data
model.fit(X_train, y_train)

# Step 9: Evaluate the Model
# Make predictions on the test data
y_pred = model.predict(X_test)

# Calculate accuracy
print("Accuracy:", accuracy_score(y_test, y_pred))

# Print detailed classification report
print(classification_report(y_test, y_pred))

# Step 10: Save the Model and Scaler for Future Use
# Save the trained model and the scaler to files
joblib.dump(model, 'firewall_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

# Step 11: Load the Model and Scaler (optional)
# To make predictions on new data in the future, load the model and scaler
model = joblib.load('firewall_model.pkl')
scaler = joblib.load('scaler.pkl')
