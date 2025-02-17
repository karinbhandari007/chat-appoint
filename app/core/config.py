from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Signetic AI Scheduler"
    VERSION: str = "1.0.0"
    
    # Add these required fields
    DATABASE_URL: str
    OPENAI_API_KEY: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings() 