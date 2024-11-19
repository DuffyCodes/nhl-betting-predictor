import pandas as pd
import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'nhl_user',
    'password': 'nhl_password',
    'database': 'nhl_predictor'
}

def load_data(table_name):
    connection = mysql.connector.connect(**db_config)
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, connection)
    connection.close()
    return df