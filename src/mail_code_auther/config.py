import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_host: str = os.getenv("REDIS_HOST", "localhost")
    redis_port: int = int(os.getenv("REDIS_PORT", 6379))
    redis_password: str = os.getenv("REDIS_PASSWORD", "")

    rabbitmq_host: str = os.getenv("RABBITMQ_HOST", "localhost")
    rabbitmq_port: int = int(os.getenv("RABBITMQ_PORT", 5672))
    rabbitmq_username: str = os.getenv("RABBITMQ_USERNAME", "admin")
    rabbitmq_password: str = os.getenv("RABBITMQ_PASSWORD", "password")

    # 验证码相关设置
    verification_code_length: int = 6
    verification_code_expire_seconds: int = 300  # 5分钟过期


settings = Settings()
