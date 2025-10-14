from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "uuid" CHAR(36) NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "email" VARCHAR(100) NOT NULL UNIQUE,
    "password" VARCHAR(200) NOT NULL,
    "phone" VARCHAR(15) NOT NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJzVlm1v2jAQx78KyqtO6qqSkraapkmUaRrTRqVuTJOqKjKJk1g4dhrbayvEd6/PeSQESq"
    "pNlDdA/neH737c+VhYMfcxFSdTgVPrQ29hMRRj/WFFP+5ZKEkqFQSJZtQ4Ku1hFDQTMkWe"
    "1GKAqMBa8rHwUpJIwplWmaIURO5pR8LCSlKM3CvsSh5iGZlEbu+0TJiPH7EoHpO5GxBM/Z"
    "U8lSI+nG4srnxKjDqdjj9/Mb5w4Mz1OFUxq/snTzLirAwA+QSiwBZihlMksV8rBTLNSy6k"
    "LGstyFThMl2/EnwcIEUBiPUxUMwDDj1zErwMPlkdEHmcAV7CJPBYLLO6qqqNasFRo6/Dm6"
    "Oz83emSi5kmBqjYWItTSCSKAs1bCuY5n0N5ihCaTvMwr8BUyf6GoyFUHGs+qgAWQB6HTUr"
    "Ro8uxSyUkX7sn55uwfh7eGNIai+Dkuvezjp+kpvszAZIK4Q4RoR2YVgG/BuIL/fim0eYIC"
    "EeeNoy1psp1mMOsxvtnVDaW1DaLSg1iE4TXQYcJsS+s0s7Opu70QGCsGyCee2GBGGGvPkD"
    "Sn13zcJtvsl33RTbcVNBDIWGDVQI+ee7d4hT4kVtWzm3bN3LqPLZy2JuW8tjJtvbrnUn65"
    "+42XP5ZbbXCzCEU97b/cHF4PLsfHCpXUwmpXKxpQfHk18v7OC/+u8UpNRhaGshhzm2trPL"
    "3GqvzXef4zTvPhiNDhBz98ME+F/2sD5R4mwGVyF++3k9aYdYC2mAnDJd4K1PPHnco0TIu7"
    "eJdQtFqBqSjoW4p3V4Rz+Gf5pcR9+vr5p/wOELrva9XpbP7SdyJQ=="
)
