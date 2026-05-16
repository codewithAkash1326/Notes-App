from pydantic_settings import BaseSettings , SettingsConfigDict

class setting(BaseSettings):
    DB_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    TOKEN_SECRET_KEY:str
    ALGORITHM:str


    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = setting()