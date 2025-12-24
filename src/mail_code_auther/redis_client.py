import redis
import json
from typing import Optional
from config import settings


class RedisClient:
    def __init__(self):
        self.client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            password=settings.redis_password,
            decode_responses=True,
            db=0,
        )

    def set_verification_code(self, email: str, code: str) -> bool:
        """存储验证码到Redis"""
        try:
            key = f"verification_code:{email}"
            # 验证码5分钟过期
            result = self.client.setex(
                name=key, time=settings.verification_code_expire_seconds, value=code
            )
            return result
        except Exception as e:
            print(f"Error setting verification code: {e}")
            return False

    def get_verification_code(self, email: str) -> Optional[str]:
        """从Redis获取验证码"""
        try:
            key = f"verification_code:{email}"
            code = self.client.get(key)
            return code
        except Exception as e:
            print(f"Error getting verification code: {e}")
            return None

    def delete_verification_code(self, email: str) -> bool:
        """删除验证码"""
        try:
            key = f"verification_code:{email}"
            result = self.client.delete(key)
            return result > 0
        except Exception as e:
            print(f"Error deleting verification code: {e}")
            return False


redis_client = RedisClient()

if __name__ == "__main__":
    # 测试Redis连接和方法
    rc = RedisClient()
    test_email = "test@example.com"
    test_code = "123456"
    rc.set_verification_code(test_email, test_code)
    retrieved_code = rc.get_verification_code(test_email)
    print(f"Retrieved code: {retrieved_code}")
    rc.delete_verification_code(test_email)
    deleted_code = rc.get_verification_code(test_email)
    print(f"Code after deletion: {deleted_code}")
