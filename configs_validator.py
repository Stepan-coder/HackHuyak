from typing import Union, List
from pydantic import BaseModel


class MetaConfigsModel(BaseModel):
    IS_PROD: Union[bool] = True


class PostgresDataBaseConfigsModel(BaseModel):
    POSTGRES_DB_USERNAME: Union[str]
    POSTGRES_DB_PASSWORD: Union[str]
    POSTGRES_DB_HOST: Union[str]
    POSTGRES_DB_PORT: Union[str]
    POSTGRES_DB_NAME: Union[str]


class APIConfigsModel(BaseModel):
    API_HOST: Union[str]
    API_PORT: Union[int]
    API_URL: Union[str, None] = None
    STATIC_DIR: Union[str]
    SECRET_KEY: Union[str]
    DOMAIN: Union[str]
    access_token_expire_minutes: Union[int, None] = None
    MEDIA_DIR: Union[str]
    MEDIA_SHORT_URL: Union[str]
    CONTENT_DIR: Union[str]
    CONTENT_SHORT_URL: Union[str]
    ROOT_DIR: Union[str]
    ANALYZES_DIR: Union[str]
    CONTRACTS_DIR: Union[str]

class AuthConfigsModel(BaseModel):
    AUTH_SECRET: Union[str]
    AUTH_COOKIE_NAME: Union[str]


class GoogleOAUTHConfigsModel(BaseModel):
    OAUTH_CLIENT_ID: Union[str]
    OAUTH_CLIENT_SECRET: Union[str]
    OAUTH_SERVER_METADATA: Union[str]
    OAUTH_CLIENT_EMAILS: Union[str]


class SMTPConfigsModel(BaseModel):
    SMTP_HOSTNAME: Union[str]
    SMTP_PORT: Union[int]
    SMTP_USERNAME: Union[str]
    SMTP_PASSWORD: Union[str]
    EMAIL_SENDER: Union[str]


class ConfigsValidator(PostgresDataBaseConfigsModel,
                       MetaConfigsModel, APIConfigsModel,
                       GoogleOAUTHConfigsModel, AuthConfigsModel,
                       SMTPConfigsModel):
    pass
