from logging import config

# ===
# LOGGING
# ===
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(levelname)s] %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "verbose",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "__main__": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "": {"level": "INFO", "handlers": ["console"], "propagate": False},
    },
}

config.dictConfig(LOGGING)
