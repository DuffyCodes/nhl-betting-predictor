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

def save_relevant_stats(stats):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()    
    
    # First, truncate the table to remove old data
    cursor.execute("TRUNCATE TABLE relevant_stats")
    
    # Prepare the SQL query for inserting each stat
    query = "INSERT INTO relevant_stats (stat) VALUES (%s)"
    
    # Insert each stat individually
    cursor.executemany(query, [(stat,) for stat in stats])
    
    # Commit the transaction and close the connection
    connection.commit()
    cursor.close()
    connection.close()
    
def read_relevant_stats():    
    connection = mysql.connector.connect(**db_config)
    query = "SELECT stat FROM relevant_stats"
    df = pd.read_sql(query, connection)
    connection.close()
    
    # Return the 'stat' column as a list of feature names
    return df['stat'].tolist()