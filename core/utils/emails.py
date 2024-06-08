from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from core.celery import app
from .loggers import general_logger

User =  get_user_model()

@app.task
def send_confirmation_email(host_name,token,email):

    send_mail(
        subject="confirmation email",
        message=f"http://{host_name}/confirmation/{email}/{token}/",
        from_email="admin@admin.com",
        recipient_list=[email],
        fail_silently=True,
    )
    general_logger.info(f"confirmation email to {email} successfully")

@app.task
def send_forget_password_email(host_name, token, email):
    # Our Emails content
    send_mail(
        subject="forget password",
        message=f"http://{host_name}/forget/{token}/",
        from_email="admin@admin.com",
        recipient_list=[email],
        fail_silently=True,
    )
    general_logger.info(f"recovery email to {email} successfully")

@app.task
def send_report_email(msg, email, comment_id):
    superusers_emails = User.objects.filter(is_superuser=True).values_list(
        "email", flat=True
    )
    send_mail(
        subject="forget password",
        message=f"email :{email}\ncomment id :{comment_id}\nmsg :{msg}",
        from_email="admin@admin.com",
        recipient_list=superusers_emails,
        fail_silently=True,
    )
    general_logger.info(f"recovery email to {superusers_emails} send successfully")