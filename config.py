import os

from dotenv import find_dotenv
from dotenv import load_dotenv


load_dotenv(find_dotenv())


class Config:
    GIT_HUB_WEBHOOK_TOKEN = os.getenv(
        "GIT_HUB_WEBHOOK_TOKEN", default="This-is-a-dummy-token"
    )
