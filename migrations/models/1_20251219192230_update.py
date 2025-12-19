from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `aerichupdatetest` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `aerichupdatetest`;"""


MODELS_STATE = (
    "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"
    "i1LhHf3t1R508B7RlVv+B8NCz4Q="
)
