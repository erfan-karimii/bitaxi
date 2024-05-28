from django.urls import path

from .views import driver_views
from account.views.customer_views import (
    CustomerLoginView,
    RegisterCustomerView,
    CustomerResetPasswordView,
    CustomerForgetPasswordView,
    CustomerVerifyForgetPasswordView,
    CustomerProfileView,
    ConfirmEmailAddress,
    ResendEmailConfirm
)

app_name = "account"

urlpatterns = [
    path("driver/signup/", driver_views.DriverSignUP.as_view(), name="DriverSignUP"),
    path("driver/signin/", driver_views.DriverLogin.as_view(), name="DriverSignIn"),
    path(
        "driver/password/reset/", driver_views.ResetPassword.as_view(), name="reset_password"
    ),
    path(
        "password/forget/",
        driver_views.ForgetPassword.as_view(),
        name="forget_password",
    ),
    path("password/forget/verify/<token>/", driver_views.VerifyForgetPassword.as_view(), name="vrify"),
    path(
        "driver/profile/", driver_views.DriverProfileView.as_view(), name="driverprofile"
    ),
]


customer_urlpatterns = [
    path("customer/login/", CustomerLoginView.as_view(), name="create-user-token"),
    path(
        "customer/register/", RegisterCustomerView.as_view(), name="register_user_view"
    ),
    path(
        "customer/reset-password/",
        CustomerResetPasswordView.as_view(),
        name="customer_reset_password",
    ),
    path(
        "customer/password/forget/",
        CustomerForgetPasswordView.as_view(),
        name="customer_forget_password",
    ),
    path(
        "customer/password/verify/<str:token>/",
        CustomerVerifyForgetPasswordView.as_view(),
        name="customer_verify_password",
    ),
    path("customer/profile/", CustomerProfileView.as_view(), name="customer_profile"),
    path("email/confirmation/<email>/<token>/", ConfirmEmailAddress.as_view(), name="confirm_email"),
    path("email/confirmation/resend/",ResendEmailConfirm.as_view(),name="resend_conf_email")
    
]


urlpatterns += customer_urlpatterns
