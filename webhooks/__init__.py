# flake8: noqa
from flask import Flask
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from config import Config


sentry_sdk.init(
    dsn="https://daa332a5889744849b88ed9d3b22f2be@o453278.ingest.sentry.io/5450166",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0,
)


app = Flask(__name__)
app.config.from_object(Config)

from webhooks import routes
