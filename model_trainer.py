from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report

def train_model(X_train, y_train, best_params):
    # Initialize the model with best parameters
    model = XGBClassifier(**best_params)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))
