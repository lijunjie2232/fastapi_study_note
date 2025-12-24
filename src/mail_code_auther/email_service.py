import json
import random
import string

from message_queue import message_queue
from redis_client import redis_client


def generate_verification_code(length: int = 6) -> str:
    """生成验证码"""
    return "".join(random.choices(string.digits, k=length))


def send_verification_code(email: str, code: str):
    """发送验证邮件的模拟实现"""
    print(f"Sending verification code to {email}")
    # 这里可以集成真实的邮件发送服务
    # 例如：smtplib, sendgrid, 或其他邮件服务

    # 模拟邮件发送过程
    import random
    import time

    import rich.progress

    with rich.progress.Progress() as progress:
        task = progress.add_task(f"[green]Sending email to {email}...", total=100)
        while not progress.finished:
            progress.update(task, advance=random.randint(5, 15))
            time.sleep(0.5)

    print(f"Verification code {code} sent successfully to {email}")


def process_email_task(ch, method, properties, body):
    """处理邮件任务的回调函数"""
    try:
        data = json.loads(body)
        email = data.get("email")
        code = data.get("code")

        # 发送邮件
        send_verification_code(email, code)

        # 手动确认消息已处理
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing email task: {e}")
        # 拒绝消息并重新入队
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def request_verification_code(email: str) -> str:
    """请求验证码"""
    code = generate_verification_code()

    # 存储验证码到Redis
    success = redis_client.set_verification_code(email, code)

    if success:
        message_queue.publish_email_task(email, code)
        print(f"Published email task for {email}")
        return code
    else:
        raise Exception("Failed to store verification code in Redis")
