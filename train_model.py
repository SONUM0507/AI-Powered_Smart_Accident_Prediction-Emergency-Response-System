import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_and_preprocess_data(file_path: str):
    """Loads dataset and preprocesses it for training."""
    logging.info(f"Loading data from {file_path}...")
    df = pd.read_csv(file_path)

    # Important columns
    columns = [
        "Weather_Condition",
        "Road_Type",
        "Vehicle_Type",
        "Traffic_Level",
        "Light_Condition",
        "Speed_kmph",
        "Driver_Age",
        "Alcohol_Involved",
        "Seatbelt_Helmet_Used",
        "Accident_Severity"
    ]

    df = df[columns]

    # Remove missing values
    df.dropna(inplace=True)

    # Encode text columns
    label_encoders = {}
    for column in df.columns:
        if df[column].dtype == 'object' or column == "Accident_Severity":
            le = LabelEncoder()
            df[column] = le.fit_transform(df[column])
            label_encoders[column] = le
            
    logging.info("Data preprocessing completed.")
    return df, label_encoders

def train_and_evaluate(df):
    """Trains a Random Forest classifier and evaluates it."""
    # Features and target
    X = df.drop("Accident_Severity", axis=1)
    y = df["Accident_Severity"]

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train model
    logging.info("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluation
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    logging.info(f"Model Accuracy: {accuracy * 100:.2f}%")
    
    return model

def save_artifacts(model, encoders, output_dir="models"):
    """Saves the trained model and label encoders."""
    os.makedirs(output_dir, exist_ok=True)
    
    model_path = os.path.join(output_dir, "accident_model.pkl")
    encoders_path = os.path.join(output_dir, "label_encoders.pkl")
    
    joblib.dump(model, model_path)
    joblib.dump(encoders, encoders_path)
    
    logging.info(f"Model saved successfully to {model_path}!")
    logging.info(f"Encoders saved successfully to {encoders_path}!")

def main():
    data_path = "vadodara_accident_dataset.csv"
    
    if not os.path.exists(data_path):
        logging.error(f"Dataset not found at {data_path}. Cannot train model.")
        return
        
    df, encoders = load_and_preprocess_data(data_path)
    model = train_and_evaluate(df)
    save_artifacts(model, encoders)

if __name__ == "__main__":
    main()