import json
from typing import Any, Dict

import pika
from config import settings


class MessageQueue:

    def __init__(self):
        self.init()

    def __enter__(self):
        self.init()
        return self

    def init(self):
        self.connection = None
        self.channel = None
        """连接到RabbitMQ"""
        try:
            credentials = pika.PlainCredentials(
                settings.rabbitmq_username, settings.rabbitmq_password
            )
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=settings.rabbitmq_host,
                    port=settings.rabbitmq_port,
                    credentials=credentials,
                )
            )
            self.channel = self.connection.channel()

            # 声明邮件队列
            self.channel.queue_declare(queue="email_verification_queue", durable=True)

        except Exception as e:
            print(f"Error connecting to RabbitMQ: {e}")
        assert self.connection and self.channel, "Failed to connect to RabbitMQ"

    def publish_email_task(self, email: str, code: str):
        """发布邮件发送任务到队列"""
        try:
            message = {"email": email, "code": code, "timestamp": self.get_timestamp()}

            self.channel.basic_publish(
                exchange="",
                routing_key="email_verification_queue",
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # 消息持久化
                ),
            )
            print(f"Email task published for {email}")
        except Exception as e:
            print(f"Error publishing email task: {e}")
            import traceback

            traceback.print_exc()

    def consume_email_tasks(self, callback_func):
        """消费邮件任务"""
        try:
            # 设置QoS，一次只处理一个消息
            self.channel.basic_qos(prefetch_count=1)

            self.channel.basic_consume(
                queue="email_verification_queue", on_message_callback=callback_func
            )

            print("Waiting for email tasks. To exit press CTRL+C")
            self.channel.start_consuming()
        except Exception as e:
            print(f"Error consuming email tasks: {e}")

    def get_timestamp(self):
        from datetime import datetime

        return datetime.now().isoformat()

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection and not self.connection.is_closed:
            self.connection.close()


message_queue = MessageQueue()

if __name__ == "__main__":
    # 测试连接和发布消息
    with MessageQueue() as mq:
        # mq.publish_email_task("test@example.com", "123456")
        mq.consume_email_tasks(
            lambda ch, method, properties, body: print(f"Received: {body}")
        )
