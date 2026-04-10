from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    database_url: str = "postgresql://neondb_owner:npg_2aXfQqmlVNb8@ep-wild-queen-amx9yl8t-pooler.c-5.us-east-1.aws.neon.tech/neondb?channel_binding=require&sslmode=require"


settings = Settings()
