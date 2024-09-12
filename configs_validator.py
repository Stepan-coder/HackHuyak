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
    ANALYZES_DIR: Union[str]

class AuthConfigsModel(BaseModel):
    AUTH_SECRET: Union[str]
    AUTH_COOKIE_NAME: Union[str]


class GoogleOAUTHConfigsModel(BaseModel):
    OAUTH_CLIENT_ID: Union[str]
    OAUTH_CLIENT_SECRET: Union[str]
    OAUTH_SERVER_METADATA: Union[str]
    OAUTH_CLIENT_EMAILS: Union[str]


# class LogsConfigModel(BaseModel):
#     LOG_FILE: Union[str, None]

#
# class SMTPConfigsModel(BaseModel):
#     SMTP_HOSTNAME: Union[str]
#     SMTP_PORT: Union[int]
#     SMTP_USERNAME: Union[str]
#     SMTP_PASSWORD: Union[str]
#     EMAIL_SENDER: Union[str]
#
#
# class PaymentsConfigsModel(BaseModel):
#     SECRET_KEY: Union[str]
#     PRICE: Union[int]
#     PUBLIC_ID: Union[str]
#     PRODUCT_NAME: Union[str]
#
#
# class OpenAIConfigModel(BaseModel):
#     OPENAI_API_KEY: Union[str, None]
#     ASSISTANT_ID: Union[str, None]
#
#
# class YandexDiskConfigModel(BaseModel):
#     YADISK_TOKEN: Union[str, None]
#     YADISK_CL_FILES_DIR: Union[str, None]


class ConfigsValidator(PostgresDataBaseConfigsModel,
                       MetaConfigsModel, APIConfigsModel,
                       GoogleOAUTHConfigsModel, AuthConfigsModel):
    pass
