from django.db import models
from account.models import CustomerProfile,User


class Discount(models.Model):
    code = models.CharField(max_length=25)
    discount = models.IntegerField()
    validate_time = models.DateTimeField()
    customer = models.ManyToManyField(CustomerProfile,through='DiscountUserProfile')

    def __str__(self):
        return "کد تخفیف "+ self.code + "با مبلغ "+ self.discount
    

class DiscountUserProfile(models.Model):
    customer_profile = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount,on_delete=models.CASCADE)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.customer_profile.full_name + "//"+ self.discount


class PayMentLog(models.Model):
    STATUS = (
        ('INCREASE','INCREASE'),
        ("DECREASE","DECREASE"),
    )
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    cost = models.IntegerField()
    day = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=25,choices=STATUS)
    message = models.CharField(max_length=360,null=True,help_text='شرح حال تراکنش')

    def __str__(self,):
        return self.id +"/"+ self.user.email +"/"+ self.cost
    
