from authlib.integrations.starlette_client import OAuth
from settings import config_parameters


oauth = OAuth()

oauth.register(
    'google',
    client_id=config_parameters.OAUTH_CLIENT_ID,
    client_secret=config_parameters.OAUTH_CLIENT_SECRET,
    server_metadata_url=config_parameters.OAUTH_SERVER_METADATA,
    client_kwargs={
        'scope': 'openid email profile',
        'prompt': 'select_account',
        'verify': False
    },
)

google = oauth.create_client('google')