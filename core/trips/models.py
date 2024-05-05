from django.db import models
from account.models import DriverProfile,CustomerProfile
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
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
        return self.driver.full_name + "/"+ self.customer.full_name()
    

class DriverOffers(models.Model):
    PROVINCE_CHOICES = (
        ('AL', _('Alborz')),
        ('AR', _('Ardabil')),
        ('AE', _('Azerbaijan East')),
        ('AW', _('Azerbaijan Wast')),
        ('BU', _('Bushehr')),
        ('CM', _('Chahar Mahaal and Bakhtiari')),
        ('FA', _('Fars')),
        ('GI', _('Gilan')),
        ('GO', _('Golestan')),
        ('HA', _('Hamadan')),
        ('HO', _('Hormozgan')),
        ('IL', _('Ilam')),
        ('IS', _('Isfahan')),
        ('KE', _('Kerman')),
        ('KM', _('Kermanshah')),
        ('KN', _('Khorasan North')),
        ('KR', _('Khorasan Razavi')),
        ('KS', _('Khorasan South')),
        ('KH', _('Khuzestan')),
        ('KB', _('Kohgiluyeh and Boyer-Ahmad')),
        ('KU', _('Kurdistan')),
        ('LO', _('Lorestan')),
        ('MA', _('Markazi')),
        ('MZ', _('Mazandaran')),
        ('QA', _('Qazvin')),
        ('QO', _('Qom')),
        ('SE', _('Semnan')),
        ('SB', _('Sistan and Baluchestan')),
        ('TH', _('Tehran')),
        ('YZ', _('Yazd')),
        ('ZN', _('Zanjan')),
    )
    driver = models.ForeignKey(DriverProfile,on_delete=models.CASCADE)
    price = models.IntegerField()
    start_offer_time = models.DateTimeField()
    end_offer_time = models.DateTimeField()
    origin = models.CharField(max_length=254,choices=PROVINCE_CHOICES)
    destination = models.CharField(max_length=254,choices=PROVINCE_CHOICES)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.driver.full_name + " " + self.origin+ " "+ self.destination

class Comment(models.Model):
    customer = models.ForeignKey(CustomerProfile,on_delete=models.PROTECT)
    driver = models.ForeignKey(DriverProfile,on_delete=models.PROTECT)
    trips = models.OneToOneField(Trips,on_delete=models.CASCADE)
    text = models.TextField(null=True,blank=True)
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.customer.full_name + " "+ self.score