import json
import os

from dotenv import find_dotenv
from dotenv import load_dotenv


load_dotenv(find_dotenv())


class MissingConfig(BaseException):
    pass


class WrongConfigFile(BaseException):
    pass


class Config:
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

    ENV = os.getenv("ENV", default="DEVELOPMENT")

    GIT_HUB_WEBHOOK_TOKEN = os.getenv(
        "GIT_HUB_WEBHOOK_TOKEN", default="This-is-a-dummy-token"
    )

    if ENV == "PRODUCTION":
        repositories_config_path = os.getenv("REPOSITORIES_CONFIG", default=CURRENT_DIR)

        try:
            with open(repositories_config_path, "r") as f:
                REPOSITORIES_CONFIG = json.load(f)
        except IsADirectoryError:
            raise MissingConfig()
        except FileNotFoundError:
            raise WrongConfigFile()
    else:
        REPOSITORIES_CONFIG = {}

    DEFAULT_BRANCH = os.getenv("DEFAULT_BRANCH", default="master")
