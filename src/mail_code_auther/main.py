from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel, EmailStr
from redis_client import redis_client
from email_service import request_verification_code
import json

app = FastAPI(debug=True)


class EmailRequest(BaseModel):
    email: EmailStr


@app.post("/send_code/")
async def send_verification_code(
    request: EmailRequest, background_tasks: BackgroundTasks
):
    """发送验证码到邮箱"""
    try:
        background_tasks.add_task(request_verification_code, request.email)
        print(f"Scheduled background task to send code to {request.email}")
        return {
            "message": "Verification code has being sent in the background.",
            "email": request.email,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to send verification code: {str(e)}"
        )


@app.post("/verify_code/")
async def verify_code(email: str, code: str):
    """验证验证码"""
    stored_code = redis_client.get_verification_code(email)

    if stored_code and stored_code == code:
        # 验证成功后删除验证码
        redis_client.delete_verification_code(email)
        return {"message": "Verification successful"}
    else:
        raise HTTPException(
            status_code=400, detail="Invalid or expired verification code"
        )


@app.get("/health")
async def health_check():
    """健康检查"""
    try:
        # 测试Redis连接
        redis_client.client.ping()

        return {"status": "healthy", "services": ["redis", "rabbitmq"]}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
    )
