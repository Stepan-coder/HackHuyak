import logging
import os
import sys

import pytz

from configs_validator import ConfigsValidator
from dotenv import load_dotenv
from pydantic import ValidationError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext


_logger = logging.getLogger(__name__)

load_dotenv(dotenv_path=os.path.join('configs', '.env'))

is_prod = os.environ.get('IS_PROD') in [1, True, 'true', 'True']

try:
    config_parameters = ConfigsValidator(**os.environ)
except ValidationError as e:
    _logger.critical(exc_info=e, msg='Env parameters validation')
    sys.exit(-1)

config_parameters.IS_PROD = is_prod

timezone = pytz.timezone('Europe/Moscow')


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/admin/login")
ALGORITHM = "HS256"


# создать папку logs, если ее нет
if not os.path.exists('logs'):
    os.makedirs('logs')