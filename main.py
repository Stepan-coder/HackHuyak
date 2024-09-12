import yaml
import uvicorn
from settings import config_parameters


if __name__ == '__main__':
    uvicorn.run(
        'web_setup:server',
        host=config_parameters.API_HOST,
        port=config_parameters.API_PORT,
        loop='uvloop',
        reload=True,
        use_colors=True,
        log_level='info',
        log_config='log_config.yaml'
    )