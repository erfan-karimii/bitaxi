from typing import Collection
from django.db import models
from account.models import DriverProfile,CustomerProfile


class City(models.Model):
    name = models.CharField(max_length=45)

    def __str__(self) -> str:
        return self.name

class Trips(models.Model):
    driver = models.ForeignKey(DriverProfile,on_delete=models.PROTECT)
    customer = models.ForeignKey(CustomerProfile,on_delete=models.PROTECT)
    driver_offers = models.OneToOneField('DriverOffers',on_delete=models.PROTECT)
    start_time = models.DateTimeField(auto_now=True)
    cost = models.IntegerField()
    discount_code = models.CharField(null=True,blank=True)
    is_end = models.BooleanField(default=False)
    is_cancel = models.BooleanField(default=False)


    def __str__(self):
        return self.driver.full_name() + "/"+ self.customer.full_name()
    

class DriverOffers(models.Model):
    driver = models.ForeignKey(DriverProfile,on_delete=models.CASCADE)
    price = models.IntegerField()
    start_offer_time = models.DateTimeField()
    end_offer_time = models.DateTimeField()
    origin = models.ForeignKey(City,on_delete=models.PROTECT,related_name='origin')
    destination = models.ForeignKey(City,on_delete=models.PROTECT,related_name='destination')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.driver.full_name + " " + self.origin+ " "+ self.destination


