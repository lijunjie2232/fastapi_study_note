import json

import pika
from email_service import process_email_task
from message_queue import message_queue

if __name__ == "__main__":
    try:
        # 启动邮件消费者服务
        message_queue.consume_email_tasks(process_email_task)
    except KeyboardInterrupt:
        print("Email consumer stopped by user")
