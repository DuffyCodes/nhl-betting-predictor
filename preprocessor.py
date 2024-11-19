from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import data_loader

selected_features = data_loader.read_relevant_stats()

def preprocess_data(data):
    X = data[selected_features]
    y = data['target']  # Target: 1 if home team wins, 0 if away team wins

    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, X_test, y_train, y_test, scaler

# Test data preprocessing function
def preprocess_test_data(data, scaler):
    # Use only selected features for consistency
    X = data[selected_features]

    # Apply the same scaling as in training
    X = scaler.transform(X)
    return X