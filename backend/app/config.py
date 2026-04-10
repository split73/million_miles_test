from pydantic_settings import BaseSettings, SettingsConfigDict
import psycopg2
from psycopg2 import OperationalError

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    database_url: str = "postgresql://neondb_owner:npg_2aXfQqmlVNb8@ep-wild-queen-amx9yl8t-pooler.c-5.us-east-1.aws.neon.tech/neondb?channel_binding=require&sslmode=require"


settings = Settings()

def check_db_connection():
    try:
        conn = psycopg2.connect(settings.database_url)
        conn.close()
        print("Successfully connected to the database!")
        return True
    except OperationalError as e:
        print(f"Failed to connect to database: {e}")
        return False

if __name__ == "__main__":
    check_db_connection()