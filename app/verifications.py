import data_loader
import preprocessor
import pickle
from sklearn.metrics import accuracy_score, classification_report

# Load the model and scaler
with open("nhl_model.pkl", "rb") as f:
    model = pickle.load(f)
with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)
df = data_loader.load_data('verification_game_stats')

# Restructure 2024-2025 data for head-to-head matchups
df['target'] = (df['GF'] > df['GA']).astype(int)

# Preprocess the 2024-2025 test data
X_test_2024_25 = preprocessor.preprocess_test_data(df, scaler)
y_test_2024_25 = df['target']
y_pred = model.predict(X_test_2024_25)

# Evaluate model on 2024-2025 data
print("Accuracy on 2024-2025 season:", accuracy_score(y_test_2024_25, y_pred))
print(classification_report(y_test_2024_25, y_pred))