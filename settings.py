
import os

OPENAI_API_KEY="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"
STORAGE="/Users/jozi/Code/shikimi/databases"

env = os.environ

env["OPENAI_API_KEY"] = OPENAI_API_KEY
env["STORAGE"] = STORAGE

QDRANT_HOST = env.get("QDRANT_HOST", "http://qdrant:6333")
SONARQUUBE_HOST = env.get("SONARQUUBE_HOST", "http://sonarqube:9000")
DATABASE_URL = env.get("POSTGRES_URL", "postgresql://techdebt:techdebt@postgres:5432/techdebt")
KEYCLOAK_SETTINGS = {
    "realm": env.get("KEYCLOAK_REALM", "TechDebtGPT"),
    "auth-server-url": env.get("KEYCLOAK_HOST", "http://keycloak:8080/auth"),
    "ssl-required": "external",
    "resource": env.get("KEYCLOAK_CLIENT_ID", "dev-TechDebtGPT"),
    "verify-token-audience": True
}

# JWT Configuration
SECRET_KEY = env.get("SECRET_KEY", "shitty.super.secret.key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES =env.get("TOKEN_EXPIRE_MINUTES", 60)
REFRESH_TOKEN_TIME_DELTA = env.get("REFRESH_TOKEN_TIME_DELTA", 5)
REDIS_URL = env.get("REDIS_URL", "redis://redis:6379")
THROTTLE_LIMIT_PER_MINUTE = env.get("THROTTLE_LIMIT_PER_MINUTE", 60)