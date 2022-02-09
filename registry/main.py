import logging
from concurrent.futures import ThreadPoolExecutor

import tempfile
import shutil

import os
import sushy
import sys
from sushy import auth
from sushy.resources import base
from sushy.resources import constants
from sushy.resources.registry import message_registry

# disable InsecureRequestWarning: Unverified HTTPS request is being made to host
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

MSG_PARSER_PORT = 9097
DOWNLOAD_DIR = '.download/'

def get_log_level(level):
    level = level.upper()
    if level == "DEBUG":
        return logging.DEBUG
    elif level == "INFO":
        return logging.INFO
    elif level == "WARNING":
        return logging.WARNING
    elif level == "ERROR":
        return logging.ERROR
    elif level == "TRACE":
        return logging.DEBUG
    else:
        logging.warning('Log level %s is not supported. Set level to DEBUG.', level)
        return logging.DEBUG

def getRegistries():
    redfish_username = os.environ.get('REDFISH_USERNAME')
    redfish_password = os.environ.get('REDFISH_PASSWORD')
    redfish_hostaddr = os.environ.get('REDFISH_HOSTADDR')

    basic_auth = auth.BasicAuth(username=redfish_username, password=redfish_password)
    try:
        sushy_root = sushy.Sushy('https://' + redfish_hostaddr + '/redfish/v1',
                                      auth=basic_auth, verify=False)
    except sushy.exceptions.ConnectionError:
        logging.error('Timeout connecting to %s', redfish_hostaddr)
        sys.exit(1)

    logging.info('Redfish version: %s', sushy_root.redfish_version)
    registries = sushy_root.lazy_registries

    # preload the registries
    logging.info('Preloading Redfish Registries...')
    try:
        registries.registries
    except sushy.exceptions.AccessError as e:
            logging.error(e)
            sys.exit(1)

    logging.info('Preloading Redfish Registries DONE')
    for r in registries:
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
            tmp_file.write(registries[r])
        os.chmod(tmp_file.name, 0o644)
        shutil.move(tmp_file.name, DOWNLOAD_DIR+r)

if __name__ == '__main__':
    l = os.environ.get('LOG_LEVEL', 'DEBUG')
    log_level= get_log_level(l)
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )
    LOG = logging.getLogger('sushy')
    # Minimize log level for sushy to improve performance
    LOG.setLevel(logging.WARNING)
    LOG.addHandler(logging.StreamHandler())

    getRegistries()