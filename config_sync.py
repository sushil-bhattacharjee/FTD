#File will implement main logic for configuration synchronization. 
#The code will read the configuration file and apply the configuration to FDM through the FDM client.
import logging
import yaml
from rich import print
import argparse

from fdm import FDMClient



def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", help="Path to the configuration file.", default='fdm.cfg')
    parser.add_argument("--debug", "-d", help="Display debug logs.", action="store_true")
    return parser.parse_args()
    
    
def init_logger(log_level=logging.INFO):
    log = logging.getLogger(__file__)
    log.setLevel(log_level)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    console_handler.setFormatter(formatter)
    log.addHandler(console_handler)
    return log
    
    
class ConfigSync:
    def __init__(self, config, log):
        self.log = log
        self.config_file = config
        self.log.info('Initializing ConfigSync class.')
        self.config = self._parse_config(config)
        self.fdm = self._init_fdm_client(self.config)
        self.log.debug('ConfigSync class initialization finished.')
    
    
    def _parse_config(self, config_file):
        self.log.info('Parsing the configuration file.')
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        self.log.debug(f'The following parameters were received: {config}')
        return config
    
    def _init_fdm_client(self, config):
        self.log.info('Initializing FDMClient class.')
        host = config.get('fdm_host')
        username = config.get('fdm_username')
        password = config.get('fdm_password')
        fdm = FDMClient(host, username=username, password=password, log=self.log)
        self.log.info('Login to FDM.')
        fdm.login()        
        return fdm
    
    
if __name__ == "__main__":
    args = parse_arguments()
    
    if args.debug:
        log = init_logger(logging.DEBUG)
    else:
        log = init_logger()
        
        
    cs = ConfigSync(config=args.config, log=log)
    # print(cs.fdm.token) #After getting and print the token, disable the print
    # cs.get_config()
    # cs.sync()
    # cs.deploy()