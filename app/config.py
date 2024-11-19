from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str 
    algorithm: str
    issuer: str
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
settings = Settings()

print(settings.database_url)




  