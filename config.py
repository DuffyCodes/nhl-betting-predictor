from os import getenv
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Ensure all required environment variables are set
required_env_vars = ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']

for var in required_env_vars:
    if not getenv(var):
        raise EnvironmentError(f"Required environment variable '{var}' is not set.")

# Database configuration sourced entirely from environment variables
db_config = {
    'host': getenv('DB_HOST'),
    'user': getenv('DB_USER'),
    'password': getenv('DB_PASSWORD'),
    'database': getenv('DB_NAME')
}
