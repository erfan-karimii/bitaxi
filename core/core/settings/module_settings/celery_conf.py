CELERY_BROKER_URL = "redis://redis-celery:6379/1"
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP  = True
CELERY_RESULT_BACKEND = "redis://redis-celery:6379/0"