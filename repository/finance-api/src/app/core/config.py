import os

DATABASE_URL = os.getenv("DATABASE_URL", "mysql://finance:finance123@localhost:3306/finance_db")
JWT_SECRET = os.getenv("JWT_SECRET", "change-me-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES", "60"))

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["src.app.core.models", "aerich.models"],
            "default_connection": "default",
        }
    },
}
