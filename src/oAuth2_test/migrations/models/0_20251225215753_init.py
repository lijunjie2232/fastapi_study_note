from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL /* id of user */,
    "username" VARCHAR(255) NOT NULL /* username of user */,
    "email" VARCHAR(255) NOT NULL /* email of user */,
    "password_hash" VARCHAR(255) NOT NULL /* hashed password of user */,
    "is_active" INT NOT NULL DEFAULT 1 /* is user active */
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztlm1r2zAQx7+KyasOutFm6Vr2Lg4b62gT6JoxKMUo9sUWkSXXkvtAyXfvnRxHjvOwhq"
    "0kg71z/ndn/e+HfJfnVqoiEPpDF3IeJq3P3nNLshTwoRE59Fosy5xOgmEjYVOZyxlpk7PQ"
    "oDpmQgNKEegw55nhSqIqCyFIVCEmchk7qZD8roDAqBhMAjkGbm5R5jKCR9DVz2wSjDmIaM"
    "Eqj+hsqwfmKbPauTRfbSKdNgpCJYpUuuTsySRKzrO5NKTGICFnBuj1Ji/IPrmb9Vl1VDp1"
    "KaXFWk0EY1YIU2v3lQxCJYkfutG2wZhOed8+7px2zj5+6pxhinUyV06nZXuu97LQEuhft6"
    "Y2zgwrMyxGx+0eck2WluD1EpavplcraSBE402EFbBNDCvBQXQX5y9RTNljIEDGhi54++Rk"
    "A7Of3avet+7VAWa9o24UXubyjvdnoXYZI7AOJH0aW0Ccpf+bAI+Pjl4BELPWArSxRYB4oo"
    "HyG1yE+P3HoL8aYq2kAXIoscGbiIfm0BNcm9v9xLqBInVNplOt70Qd3sFl91eTa+9i4FsK"
    "Sps4t2+xL/CRMY3M8aT28ZMwYuHkgeVRsBRRbbUudzmUttOmwiSLLSvqmPqbLZGhtgN9ab"
    "lYfeNqKaqM/4vl91cPLXhq7FXMdr9gyIl93mI41mt2PCHnXrak+vYLB1LGxTZU5wW7RmqN"
    "7B3PjGn9oHDMJUwn23BdKtw1X/IBkVf52jvSXAc4xvn9ipngKyWAyTXTtV7XgDzCwreiPJ"
    "+8i4NWW6qes/RH+94fDC4W9r1/ft1gOrz0v+DfKosak7gBN4J3uuWnL4XEjBI="
)
