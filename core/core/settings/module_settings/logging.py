
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{name}:{levelname} [{asctime}] {pathname}:{lineno} -> {module} - '{message}'",
            "style": "{",
        },
        "simple": {
            "format": "{name}:{levelname} [{asctime}] '{message}'",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
        },
        "general-file": {
            "class": "logging.FileHandler",
            "level": "INFO",
            "filename": "info.log",
            "formatter": "simple",
        },
        "error-file": {
            "class": "logging.FileHandler",
            "level": "ERROR",
            "filename": "error.log",
            "formatter": "verbose",
        },
    },
    # "root": {
    #     "handlers": ["console"],
    #     "level": "INFO",
    # },
    "loggers": {
        "": {"handlers": ["console", "general-file"], "level": "INFO"},
        "error": {"handlers": ["error-file"], "level": "ERROR"},
    },
}
