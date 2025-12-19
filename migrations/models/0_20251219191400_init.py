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
CREATE TABLE IF NOT EXISTS `groups` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary key field with auto increment',
    `name` VARCHAR(100) NOT NULL UNIQUE COMMENT 'Group name with maximum length of 100 characters and unique constraint'
) CHARACTER SET utf8mb4 COMMENT='Group table';
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary key field with auto increment',
    `username` VARCHAR(255) NOT NULL UNIQUE COMMENT 'Username field with maximum length of 255 characters and unique constraint',
    `email` VARCHAR(255) NOT NULL UNIQUE,
    `age` INT NOT NULL COMMENT 'Age field as an integer, optional' DEFAULT 0,
    `amount` INT NOT NULL COMMENT 'Amount field as an integer, optional' DEFAULT 0,
    `password` VARCHAR(255) NOT NULL,
    `is_active` BOOL NOT NULL DEFAULT 1,
    `is_superuser` BOOL NOT NULL DEFAULT 0,
    `created_at` DATETIME(6) COMMENT 'Creation timestamp' DEFAULT CURRENT_TIMESTAMP(6)
) CHARACTER SET utf8mb4 COMMENT='User table';
CREATE TABLE IF NOT EXISTS `orders` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary key field with auto increment',
    `order_number` VARCHAR(100) NOT NULL UNIQUE COMMENT 'Order number with maximum length of 100 characters and unique constraint',
    `total_amount` INT NOT NULL COMMENT 'Total amount for the order',
    `is_paid` BOOL NOT NULL DEFAULT 0,
    `user_id` INT NOT NULL COMMENT 'Foreign key field to link to User model',
    CONSTRAINT `fk_orders_users_411bb784` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='Order table';
CREATE TABLE IF NOT EXISTS `user_info` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary key field with auto increment',
    `full_name` VARCHAR(255) NOT NULL COMMENT 'Full name of the user',
    `address` VARCHAR(500) NOT NULL COMMENT 'Address of the user',
    `phone_number` VARCHAR(20) NOT NULL COMMENT 'Phone number of the user',
    `user_id` INT NOT NULL UNIQUE COMMENT 'Foreign key field to link to User model',
    CONSTRAINT `fk_user_inf_users_f7a4c25a` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='User Info table';
CREATE TABLE IF NOT EXISTS `groups_users` (
    `groups_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    UNIQUE KEY `uidx_groups_user_groups__403fc9` (`groups_id`, `user_id`)
) CHARACTER SET utf8mb4 COMMENT='Many-to-Many relationship to User model';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "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"
)
