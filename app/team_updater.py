import requests
import pandas as pd
from bs4 import BeautifulSoup
import mysql.connector
import numpy as np
from config import db_config

# Define URLs for each game state
url = "https://www.naturalstattrick.com/teamtable.php?fromseason=20242025&thruseason=20242025&stype=2&sit=all&score=all&rate=n&team=all&loc=B&gpf=25&fd=&td="

# Connect to MySQL
def connect_to_db():
    return mysql.connector.connect(**db_config)

def save_game_data(game_data):
    connection = connect_to_db()
    cursor = connection.cursor()
    game_data = tuple(map(lambda x: int(x) if isinstance(x, (np.integer, np.int64)) else float(x) if isinstance(x, (np.float64, float)) else x, game_data))

    # SQL Insert statement
    insert_query = """
    INSERT INTO verification_game_stats (Team, SF,	SA,	SF_pct,	GF,	GA,	GF_pct,	xGF,	xGA,	xGF_pct,	SCF,	SCA,	SCF_pct,	SCSF,	SCSA,	SCSF_pct,	SCGF,
	SCGA,	SCGF_pct,	SCSH_pct,	SCSV_pct,	HDSF,		HDSA,	HDSF_pct,	HDGF,	HDGA,	HDGF_pct,	HDSH_pct,	HDSV_pct,	MDSF,	MDSA,	MDSF_pct,	MDGF,
	MDGA,	MDGF_pct,	MDSH_pct,	MDSV_pct,	LDSF,	LDSA,	LDSF_pct,	LDGF,	LDGA,	LDGF_pct,	LDSH_pct,	LDSV_pct,	SH_pct,	SV_pct)
    VALUES (%s, %s, %s, %s, %s,  %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s,  %s, %s,  %s,  %s,  %s,  %s, %s, %s, %s, %s,  %s,  %s,  %s,  %s, 
        %s, %s,  %s, %s, %s, %s, %s,  %s,  %s, %s, %s,  %s,  %s,  %s, %s)
    """

    cursor.execute(insert_query, game_data)
    connection.commit()
    cursor.close()
    connection.close()

def safe_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0

# Function to scrape stats for a particular game situation
def scrape_stats():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table
    table = soup.find_all('table')
    # table.find_all('thead').find_all('th')[0]='trash'
    # tableheaders[0] = 'trash'
    # Extract headers
    # headers = [th.get_text(strip=True) for th in table.find('thead').find_all('th')]
    # headers[0] = 'trash'  # Rename the first column to 'Team'
    
    # Extract rows of data
    # rows = []
    # for row in table.find('tbody').find_all('tr'):
    #     cells = [td.get_text(strip=True) for td in row.find_all('td')]
    #     rows.append(cells)
    
    # data = pd.DataFrame(rows, columns=headers)  
    df = pd.read_html(str(table))[0]
    df.rename(columns={df.columns[0]: 'trash'}, inplace=True)
    return df
# data

# Fetch and merge data for all game situations
df = scrape_stats()

df.drop(columns=['trash', 'GP','TOI','W','L','OTL','ROW','Points', 'Point %', 
                 'CF', 'CA', 'CF%','FF','FA','FF%','HDCF','HDCA','HDCF%',
                 'MDCF','MDCA','MDCF%','LDCA','LDCF','LDCF%','PDO'], inplace=True)
print(df.iterrows())

processed_rows = []
errored_rows = []
for index, row in df.iterrows():
    try:
        game_data = (
            row['Team'],
            int(safe_float(row['SF'])), int(safe_float(row['SA'])), int(safe_float(row['SF%'])), 
            int(safe_float(row['GF'])), int(safe_float(row['GA'])), int(safe_float(row['GF%'])), 
            int(safe_float(row['xGF'])), int(safe_float(row['xGA'])), int(safe_float(row['xGF%'])), 
            int(safe_float(row['SCF'])), int(safe_float(row['SCA'])), int(safe_float(row['SCF%'])), 
            int(safe_float(row['SCSF'])), int(safe_float(row['SCSA'])), int(safe_float(row['SCSF%'])), 
            int(safe_float(row['SCGF'])), int(safe_float(row['SCGA'])), int(safe_float(row['SCGF%'])), int(safe_float(row['SCSH%'])), 
            int(safe_float(row['SCSV%'])), int(safe_float(row['HDSF'])), int(safe_float(row['HDSA'])), 
            int(safe_float(row['HDSF%'])), int(safe_float(row['HDGF'])),  int(safe_float(row['HDGA'])), 
            int(safe_float(row['HDGF%'])), int(safe_float(row['HDSH%'])), int(safe_float(row['HDSV%'])), 
            int(safe_float(row['MDSF'])), int(safe_float(row['MDSA'])), int(safe_float(row['MDSF%'])),
            int(safe_float(row['MDGF'])), int(safe_float(row['MDGA'])), int(safe_float(row['MDGF%'])),
            int(safe_float(row['MDSH%'])), int(safe_float(row['MDSV%'])), int(safe_float(row['LDSF'])), 
            int(safe_float(row['LDSA'])), int(safe_float(row['LDSF%'])), int(safe_float(row['LDGF'])), 
            int(safe_float(row['LDGA'])), int(safe_float(row['LDGF%'])), int(safe_float(row['LDSH%'])), 
            int(safe_float(row['LDSV%'])), int(safe_float(row['SH%'])), int(safe_float(row['SV%']))
        )
        processed_rows.append(game_data)
        
    except ValueError as e:
        errored_rows.append((index, row.to_dict(), str(e))) 
                
    print(errored_rows)
                

    # Insert data into the database
for game_data in processed_rows:
    save_game_data(game_data)