import data_loader
import feature_selection
import hyperparameter_tuner
import model_trainer
import pickle
import preprocessor

# Load data
df = data_loader.load_data('historical_game_stats')

# Merge tables into one DataFrame
# Restructure data into head-to-head format
df['target'] = (df['GF'] > df['GA']).astype(int)

##################################################################
#
#   Feature selection. comment/uncomment as needed.
#
##################################################################
X = df.drop(columns=['target','GA','GF','GF_pct'
                     #,'','','','','','','','','','','',''
                     ])
y = df['target']
# Rerun correlation analysis
feature_selection.correlation_analysis(X)

# Rerun feature importance
importance_df = feature_selection.feature_importance_analysis(X, y)
print("Feature Importance:\n", importance_df)

# Rerun RFE for feature selection
selected_features = feature_selection.recursive_feature_elimination(X, y, n_features=10)
print("Selected Features for Head-to-Head Model:", selected_features)
data_loader.save_relevant_stats(selected_features)

##################################################################
#
#   Model training. comment/uncomment as needed.
#
##################################################################

# Preprocess the training data
X_train, X_test, y_train, y_test, scaler = preprocessor.preprocess_data(df)

# Hyperparameter tuning (optional)
best_params = hyperparameter_tuner.tune_hyperparameters(X_train, y_train, X_test, y_test)
print("Best Parameters:", best_params)

# Train and evaluate model
model = model_trainer.train_model(X_train, y_train, best_params)
model_trainer.evaluate_model(model, X_test, y_test)


# Save the model
with open("nhl_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)
    
print("Tuned model and scaler saved to 'nhl_model_tuned.pkl' and 'scaler.pkl'")

###################################################################