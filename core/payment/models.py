from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from account.models import CustomerProfile, User

# from django.db.models.functions import Now
from django.utils import timezone


class Discount(models.Model):
    code = models.CharField(max_length=25, unique=True)
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    validate_time = models.DateTimeField()
    customer = models.ManyToManyField(CustomerProfile, through="DiscountUserProfile")

    def __str__(self):
        return "کد تخفیف " + self.code + "با مبلغ " + str(self.discount)

    def is_still_valid(self):
        return self.validate_time > timezone.now()


class DiscountUserProfile(models.Model):
    customer_profile = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.customer_profile.full_name + "//" + self.discount


class PayMentLog(models.Model):
    STATUS = (
        ("INCREASE", "INCREASE"),
        ("DECREASE", "DECREASE"),
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    cost = models.IntegerField()
    day = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=25, choices=STATUS)
    message = models.CharField(max_length=360, null=True, help_text="شرح حال تراکنش")

    def __str__(
        self,
    ):
        return self.id + "/" + self.user.email + "/" + self.cost
