import pandas as pd
import mysql.connector
import hashlib
import numpy as np

# Database connection configuration
db_config = {
    'host': 'localhost',   # or 'db' if running within Docker network
    'user': 'nhl_user',
    'password': 'nhl_password',
    'database': 'nhl_predictor'
}

# Connect to MySQL
def connect_to_db():
    return mysql.connector.connect(**db_config)

# Function to save game data to MySQL
def save_game_data(game_data):
    connection = connect_to_db()
    cursor = connection.cursor()
    game_data = tuple(map(lambda x: int(x) if isinstance(x, (np.integer, np.int64)) else float(x) if isinstance(x, (np.float64, float)) else x, game_data))

    # SQL Insert statement
    insert_query = """
    INSERT INTO verification_game_stats (SF,	SA,	SF_pct,	GF,	GA,	GF_pct,	xGF,	xGA,	xGF_pct,	SCF,	SCA,	SCF_pct,	SCSF,	SCSA,	SCSF_pct,	SCGF,
	SCGA,	SCGF_pct,	SCSH_pct,	SCSV_pct,	HDSF,		HDSA,	HDSF_pct,	HDGF,	HDGA,	HDGF_pct,	HDSH_pct,	HDSV_pct,	MDSF,	MDSA,	MDSF_pct,	MDGF,
	MDGA,	MDGF_pct,	MDSH_pct,	MDSV_pct,	LDSF,	LDSA,	LDSF_pct,	LDGF,	LDGA,	LDGF_pct,	LDSH_pct,	LDSV_pct,	SH_pct,	SV_pct)
    VALUES (%s, %s, %s, %s, %s,  %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s,  %s, %s,  %s,  %s,  %s,  %s, %s, %s, %s, %s,  %s,  %s,  %s,  %s, 
        %s, %s,  %s, %s, %s, %s, %s,  %s,  %s, %s, %s,  %s,  %s,  %s)
    """

    cursor.execute(insert_query, game_data)
    connection.commit()
    cursor.close()
    connection.close()

# Generate a unique game_id based on date and teams
def generate_game_id(game_date, home_team, away_team):
    unique_str = f"{game_date}_{home_team}_{away_team}"
    return int(hashlib.md5(unique_str.encode()).hexdigest(), 16) % (10 ** 8)

def safe_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0

# Function to load and process the Excel data
def process_game_data(file_path):
    df = pd.read_excel(file_path)
    processed_rows = []
    errored_rows =[]

    # Loop through rows in pairs (away, then home team)
    for index, row in df.iterrows():
        try:
            game_data = (
                int(safe_float(row['SF'])), int(safe_float(row['SA'])), int(safe_float(row['SF%'])), 
                int(safe_float(row['GF'])), int(safe_float(row['GA'])), int(safe_float(row['GF%'])), 
                int(safe_float(row['xGF'])), int(safe_float(row['xGA'])), int(safe_float(row['xGF%'])), 
                int(safe_float(row['SCF'])), int(safe_float(row['SCA'])), int(safe_float(row['SCF%'])), 
                int(safe_float(row['SCSF'])), int(safe_float(row['SCSA'])), int(safe_float(row['SCSF%'])), 
                int(safe_float(row['SCGF'])), int(safe_float(row['SCGA'])), int(safe_float(row['SCGF%'])), 
                int(safe_float(row['SCSH%'])), int(safe_float(row['SCSV%'])), int(safe_float(row['HDSF'])), 
                int(safe_float(row['HDSA'])), int(safe_float(row['HDSF%'])), int(safe_float(row['HDGF'])),  
                int(safe_float(row['HDGA'])), int(safe_float(row['HDGF%'])), int(safe_float(row['HDSH%'])), 
                int(safe_float(row['HDSV%'])), int(safe_float(row['MDSF'])), int(safe_float(row['MDSA'])), 
                int(safe_float(row['MDSF%'])), int(safe_float(row['MDGF'])), int(safe_float(row['MDGA'])), 
                int(safe_float(row['MDGF%'])), int(safe_float(row['MDSH%'])), int(safe_float(row['MDSV%'])), 
                int(safe_float(row['LDSF'])), int(safe_float(row['LDSA'])), int(safe_float(row['LDSF%'])), 
                int(safe_float(row['LDGF'])), int(safe_float(row['LDGA'])), int(safe_float(row['LDGF%'])), 
                int(safe_float(row['LDSH%'])), int(safe_float(row['LDSV%'])), int(safe_float(row['SH%'])), int(safe_float(row['SV%']))
            )
            processed_rows.append(game_data)
            
        except ValueError as e:
            errored_rows.append((index, row.to_dict(), str(e))) 
                
    print(errored_rows)
                

    # Insert data into the database
    for game_data in processed_rows:
        save_game_data(game_data)

# Run the script with the provided file path
process_game_data('raw_game_data.xlsx')
