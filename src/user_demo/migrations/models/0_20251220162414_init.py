from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `email` VARCHAR(100) NOT NULL UNIQUE,
    `sex` VARCHAR(10),
    `age` INT,
    `is_active` BOOL NOT NULL DEFAULT 1,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
) CHARACTER SET utf8mb4 COMMENT='User model';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztl21P2zAQx7+KlVdFYhV0lCHepdCJTrRFkG4TD4rcxE2tJk6JHaBCfPfdOUmTJm3XTi"
    "BAGm9Izv873/1i+9xnIwhd5su6ySLujI1j8mwIGjB4KI3sEoNOp7kdDYoOfS2luWYoVUQd"
    "BdYR9SUDk8ukE/Gp4qEAq4h9H42hA0IuvNwUC34fM1uFHlNjFsHAzR2YuXDZE5PZ63Rijz"
    "jz3YVUuYtza7utZlNt6wj1XQtxtqHthH4ciFw8nalxKOZqLhRaPSZYRBXD8CqKMX3MLq0z"
    "qyjJNJckKRZ8XDaisa8K5W7IwAkF8oNspC7Qw1m+NPYPvh0cfT08OAKJzmRu+faSlJfXnj"
    "hqAj3LeNHjVNFEoTHm3B5YJDGlCryTMY2W0yu4lBBC4mWEGbB1DDNDDjFfOK9EMaBPts+E"
    "p3CBN5rNNcx+mpcnZ+ZlDVQ7WE0IizlZ4710qJGMIdgcJG6NLSCm8s8JcH9vbwOAoFoJUI"
    "8tAoQZFUv24CLEH1f93nKIBZcSyIGAAm9c7qhd4nOp7j4m1jUUsWpMOpDy3i/Cq3XN32Wu"
    "J+f9lqYQSuVFOooO0ALGeGSOJoXNj4YhdSaPNHLtykjYCFdpq0NBIyhbqKCeZoUVY31pEx"
    "lIFnXxcVmHyQfXNpkYZHKjHmNgRBJkIYtfwrBlHAQ0mtm3IleRiE0BHKwmUBFKcCrCBYE+"
    "RORMKhbUb4WpIMgwVkwe3woCf9wlNfiWO8fkIuIYk0zYrJ6MYQQsk9RgalAM9LLKzeFIB8"
    "f31IMFlPsleWKjrgvJySU+kj1lHlfwWBXA18hyNL1ls3JpA0n+ALJhGPoYSFEVS6ge9g/V"
    "PHjuBXqS6FN/J2K4p2yqSA3aDFM8YBDEgn9S0WCKU2pHLYTPUzf+t/r3aPXZytumTRV9Xq"
    "dXvTnFhU7V3KRRNVf3qWalTekNuQ3CucNn5PcmnR7OrG0ApvJ/wpfCeceb0kb41tCr3DO9"
    "JRt45fGXqv9+/n0Mdq9yAhY6RdbaqsRa0OoYFSuaRtGvxA575FtdJudb+bUvk61+/3zhMt"
    "nqWKUlN+i22rAU9UoEEVdsOdO83Vehnqbtf8VtfcGzhDW7OdSzh495YTegBrcv/Fn6tdYw"
    "tzrd9pVldi8WwJ+aVhtHGto6K1lrh6WTYB6E/OpYZwRfyXW/1y5f9uc669rAnGisQluEjz"
    "bcHPOFlVkzMO/72+DlD6Xe6RE="
)
