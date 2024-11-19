import data_loader
import feature_selection

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
