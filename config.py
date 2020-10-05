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

    DEBUG = os.getenv("DEBUG", default=True)

    GIT_HUB_WEBHOOK_TOKEN = os.getenv(
        "GIT_HUB_WEBHOOK_TOKEN", default="This-is-a-dummy-token"
    )

    if ENV == "PRODUCTION":
        try:
            repositories_config_path = os.environ["REPOSITORIES_CONFIG"]
        except KeyError:
            raise MissingConfig("REPOSITORIES_CONFIG is missing.")
    else:
        repositories_config_path = os.path.join(CURRENT_DIR, "config_repositories.json")

    try:
        with open(repositories_config_path, "r") as f:
            REPOSITORIES_CONFIG = json.load(f)
    except IsADirectoryError:
        raise MissingConfig("The given config directory is missing")
    except FileNotFoundError:
        raise WrongConfigFile("The given configuration file is missing")

    DEFAULT_BRANCH = os.getenv("DEFAULT_BRANCH", default="master")
