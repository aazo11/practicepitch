import os
from typing import Optional

class Settings:
    def __init__(self):
        self.environment = os.getenv("ENVIRONMENT", "local")
        self.debug = os.getenv("DEBUG", "True").lower() == "true"
        
        # Database
        self.database_url = self._get_database_url()
        
        # Email settings
        self.email_backend = os.getenv("EMAIL_BACKEND", "console")
        self.smtp_host = os.getenv("SMTP_HOST", "localhost")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@practicepitch.local")
        
        # Zoom settings
        self.zoom_api_key = os.getenv("ZOOM_API_KEY", "")
        self.zoom_api_secret = os.getenv("ZOOM_API_SECRET", "")
        
        # Security
        self.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
        self.allowed_hosts = os.getenv("ALLOWED_HOSTS", "*").split(",")

    def _get_database_url(self) -> str:
        if self.environment == "production":
            return os.getenv(
                "DATABASE_URL", 
                "postgresql://username:password@localhost:5432/practicepitch_prod"
            )
        else:
            return os.getenv("DATABASE_URL", "sqlite:///./local.db")

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def is_local(self) -> bool:
        return self.environment == "local"

# Global settings instance
settings = Settings() 