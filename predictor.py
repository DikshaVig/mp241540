import os
import joblib
import numpy as np

# Load pre-trained .pkl files generated from Google Colab
MODEL_PATH = os.path.join('model', 'model.pkl')
SCALER_PATH = os.path.join('model', 'scaler.pkl')

def predict_segment(gender, age, income, spending):
    """
    Encodes gender, scales inputs using scaler.pkl, 
    and predicts cluster using model.pkl.
    """
    # 1. Convert categorical input to numeric (Male = 1, Female = 0)
    gender_numeric = 1 if str(gender).strip().lower() == 'male' else 0

    # 2. Reshape into 2D array matching model input shape: [Gender, Age, Income, Spending]
    features = np.array([[gender_numeric, age, income, spending]])

    # 3. Load Colab models and predict
    if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
        scaler = joblib.load(SCALER_PATH)
        model = joblib.load(MODEL_PATH)
        
        # Scale features using StandardScaler from Colab
        scaled_features = scaler.transform(features)
        
        # Predict cluster ID
        cluster_id = model.predict(scaled_features)[0]
        return int(cluster_id)
    else:
        # Fallback heuristic logic if .pkl files are temporarily missing
        if income > 70 and spending > 60:
            return 1
        elif income > 70 and spending <= 40:
            return 0
        elif income <= 40 and spending > 60:
            return 2
        elif income <= 40 and spending <= 40:
            return 3
        else:
            return 4