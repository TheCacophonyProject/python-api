import logging
import json
from pathlib import Path

import attr

CONFIG_FILE = "defaultconfig.json"


@attr.s
class Config:
    api_url = attr.ib(default="http://127.0.0.1:1080")
    admin_username = attr.ib(default="admin_test")
    admin_password = attr.ib(default="admin_test")
    admin_email = attr.ib(default="admin@email.com")
    default_group = attr.ib(default="test-group")
    fileprocessing_url = attr.ib(default="http://127.0.0.1:2008")
    # config_file=attr.ib(default=CONFIG_FILE)
    # self.config_file=CONFIG_FILE



    def load_config(self, **kwargs):
        if "config_file" in kwargs:
            logging.debug("config_file offered")
            self.config_file = kwargs['config_file']
        else:
            self.config_file = CONFIG_FILE
        if not Path(self.config_file).is_file():
            logging.info("No config file '{}'.  Running with default config.".format(self.config_file))
            return self

        logging.info("Attempting to load config from file '{}'...".format(self.config_file))
        with open(self.config_file) as f:
            returnResult = Config(**json.load(f))
            logging.debug("Returned Config: {}".format(returnResult))
            return returnResult

    def save_config(self):
        if not Path(self.config_file).is_file():
            logging.info("No config file '{}'.  saving current config.".format(self.config_file))
            logging.info("Attempting to save config to file '{}'...".format(self.config_file))
            try:
                with open(self.config_file,mode = 'w') as f:
                    f.write(json.dumps(attr.asdict(t), sort_keys=True, indent=4))
                return True
            except:
                return False
        else:
            return False
