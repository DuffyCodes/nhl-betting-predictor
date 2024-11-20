import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_selection import RFE
from xgboost import XGBClassifier

# Correlation Analysis
def correlation_analysis(data):
    # Select only numeric columns for correlation analysis
    numeric_data = data.select_dtypes(include=['number'])
    
    # Calculate and plot the correlation matrix
    plt.figure(figsize=(12, 8))
    correlation_matrix = numeric_data.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
    plt.title("Feature Correlation Matrix")
    plt.show()


# Feature Importance using XGBoost
def feature_importance_analysis(X, y):
    # Ensure only numeric columns are selected
    X_numeric = X.select_dtypes(include=['number'])

    # Fit XGBoost model
    model = XGBClassifier()
    model.fit(X_numeric, y)

    # Plot feature importance
    plt.figure(figsize=(10, 6))
    plt.barh(X_numeric.columns, model.feature_importances_)
    plt.xlabel("Feature Importance")
    plt.title("Feature Importance from XGBoost")
    plt.show()

    # Return features sorted by importance
    importance_df = pd.DataFrame({'Feature': X_numeric.columns, 'Importance': model.feature_importances_})
    return importance_df.sort_values(by="Importance", ascending=False)



# Recursive Feature Elimination (RFE)
def recursive_feature_elimination(X, y, n_features=10):
    X_numeric = X.select_dtypes(include=['number'])
    model = XGBClassifier()
    rfe = RFE(model, n_features_to_select=n_features)
    rfe.fit(X_numeric, y)

    # Get the selected features
    selected_features = X_numeric.columns[rfe.support_]
    print("Selected Features by RFE:", selected_features)
    return selected_features

