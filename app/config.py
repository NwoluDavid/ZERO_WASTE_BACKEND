import secrets
from typing import Annotated, Any, Literal
from typing import Optional 
from fastapi_mail import ConnectionConfig

from pydantic import (
    AnyUrl,
    BeforeValidator,
    computed_field,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    MAIL_FROM_NAME: str = "ZERO WASTE"
    FORGET_PASSWORD_LINK_EXPIRE_MINUTES: int =10
    
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []
    
    ALGORITHM: str = "HS256"
    
    conf:Any = ConnectionConfig( 
        MAIL_USERNAME = "monkado4life@yahoo.com",
        MAIL_PASSWORD = "moncado007",
        MAIL_FROM = "monkado4life@yahoo.com",
        MAIL_PORT = "587",
        MAIL_SERVER = "smtp.mail.yahoo.com",
        MAIL_FROM_NAME = "",
        MAIL_STARTTLS = True,
        MAIL_SSL_TLS = False,
        USE_CREDENTIALS = True,
        VALIDATE_CERTS = True
    )




settings = Settings()