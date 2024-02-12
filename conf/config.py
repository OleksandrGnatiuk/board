# from pydantic import ConfigDict
# from pydantic_settings import BaseSettings
#
#
# class Settings(BaseSettings):
#     token: str = "jhggfdss"
#     sqlalchemy_database_url: str = "postgresql+asyncpg://postgres:password@localhost:5432/todo_db"
#     redis_host: str = 'localhost'
#     redis_port: int = 6379
#
#     model_config = ConfigDict(extra='ignore', env_file=".env", env_file_encoding="utf-8")
#
#
# settings = Settings()