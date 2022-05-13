from pydantic import BaseModel, BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str = "localhost"
    database_name:str
    database_username: str = "postgres"
    secret_key_admin:str ="berhbvteghrvbreiva"
    secret_key_subadmin:str ="berhbvteghrvbreivb"
    secret_key_user:str ="berhbvteghrvbreivc"
    algorithm :str
    access_token_expire_minutes:int

    class Config:
        env_file= ".env"

settings = Settings()   
print(settings.database_password)