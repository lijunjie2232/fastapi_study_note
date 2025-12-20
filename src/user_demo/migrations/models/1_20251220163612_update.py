from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `users` ADD `password` VARCHAR(100) NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `users` DROP COLUMN `password`;"""


MODELS_STATE = (
    "eJztl21P2zAQx7+KlVdFYhV0FBDvWugEE20RtNvEgyI3cVOLxA6xA1SI7747J2nS9GHtVA"
    "Ro4w3J+X/nu19sn/tiBdJlvqo2WMSdkXVEXixBAwYPpZFtYtEwzO1o0HTgGynNNQOlI+po"
    "sA6prxiYXKaciIeaSwFWEfs+GqUDQi683BQL/hAzW0uP6RGLYODmDsxcuOyZqew1vLeHnP"
    "nuVKrcxbmN3dbj0NjOhP5mhDjbwHakHwciF4djPZJiouZCo9VjgkVUMwyvoxjTx+zSOrOK"
    "kkxzSZJiwcdlQxr7ulDuigwcKZAfZKNMgR7O8qW2u3ewd/h1f+8QJCaTieXgNSkvrz1xNA"
    "Q6PevVjFNNE4XBmHN7ZJHClGbgHY9oNJ9ewaWEEBIvI8yALWOYGXKI+cLZEMWAPts+E57G"
    "BV6r15cw+9G4PD5tXFZAtYXVSFjMyRrvpEO1ZAzB5iBxa6wBMZV/ToC7OzsrAATVQoBmbB"
    "ogzKhZsgenIX6/6nbmQyy4lED2BRR443JHbxOfK333MbEuoYhVY9KBUg9+EV6l3fhV5np8"
    "3m0aClJpLzJRTIAmMMYjc3hf2PxoGFDn/olGrj0zImtykXZ2KKgFZQsV1DOssGKsL20ifc"
    "WiNj7O6zD54NImE4NMrdRjLIxIgixk8UtYtoqDgEZj+1bkKhKxEMDBagIVoQSnIlwQ6ENE"
    "jZVmQfVWNDQEGcSaqaNbQeCPu6QC33LriFxEHGOSezauJmMYAcskFZgaFH2zrHKzHJrg+J"
    "56sIByvyRPbNR1ITk1x0ex58zjCh5nBfA1shwb3rxZubKBJH8E2UBKHwNpqmMF1cP+oYYH"
    "z71ATxJ96u9EDPeUTTWpQJthmgcMgvTgn9I0CHFK42iE8Hmq1v9W/x6tPlt567Spos9met"
    "WbU5zqVPVVGlV9cZ+qz7QpsyHXQThx+Iz83qTTw5m1DsBU/lf4UjjveFNaCd8SejP3TG/O"
    "Bl54/KXqP59/H4PdRk7AQqfIWtsssSa0OkbFgqZR9Cuxwx75VpfJyVbe9GWy2e2eT10mm2"
    "e90pLrt5stWIpmJYKIazafad7uZ6GepO1/wW19yrOENbs5VLOHj3lht6AGtyv8cfq1ljDv"
    "nbVbV71G+2IK/Emj18KRmrGOS9bKfukkmAQhP896pwRfyXW30ypf9ie63rWFOdFYS1vIJx"
    "tujvnCyqwZmKkPG1KlnmQ053K1+Ggu+vzjP2Xf9WfW62/cXlKj"
)
