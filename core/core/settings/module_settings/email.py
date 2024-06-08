from decouple import config


ADMIN_EMAIL = config("ADMIN_EMAIL",default="admin@admin.com")
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = False
EMAIL_HOST = config("EMAIL_HOST",default="smtp4dev")
EMAIL_HOST_USER = config("EMAIL_HOST_USER",default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD",default="")
EMAIL_PORT = 25