# LMS settings with xAPI enabled
from docker_run_production import *
from .utils import Configuration

# Load custom configuration parameters from yaml files
config = Configuration(os.path.dirname(__file__))

DEBUG = True
REQUIRE_DEBUG = True

EMAIL_BACKEND = config(
    "EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)

PIPELINE_ENABLED = False
STATICFILES_STORAGE = "openedx.core.storage.DevelopmentStorage"

ALLOWED_HOSTS = ["*"]

WEBPACK_CONFIG_PATH = "webpack.dev.config.js"

INSTALLED_APPS += ["xapi"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {"xapi": {"handlers": ["console"], "level": "DEBUG"}},
}

EVENT_TRACKING_BACKENDS = {
    "xapi_tracking_logs": {
        "ENGINE": "eventtracking.backends.routing.RoutingBackend",
        "OPTIONS": {
            "backends": {"xapi": {"ENGINE": "xapi.backend.xAPIBackend", "OPTIONS": {}}},
            "processors": [],
        },
    }
}
