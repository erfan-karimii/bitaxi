from django.core.mail import send_mail
from .loggers import general_logger


def send_confirmation_email(request,token,email):

    host_name = request.get_host()
    send_mail(
        subject="confirmation email",
        message=f"http://{host_name}/confirmation/{email}/{token}/",
        from_email="admin@admin.com",
        recipient_list=[email],
        fail_silently=True,
    )
    general_logger.info(f"confirmation email to {email} successfully")