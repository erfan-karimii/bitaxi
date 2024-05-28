from PIL import Image
from io import BytesIO
from base64 import b64encode

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.arvan_bucket_conf import bucket
# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model
    """

    email = models.EmailField(max_length=254, unique=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    is_driver = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    Token = models.IntegerField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return self.email


class BaseProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    cash_bank = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.email + "//" + self.first_name + "//" + self.last_name

    @property
    def full_name(self) -> str:
        return self.first_name + " " + self.last_name

    class Meta:
        abstract = True


class DriverProfile(BaseProfile):
    CARS = (("SAMAND", "SAMAND"), ("PEUGEOT", "PEUGEOT"))
    STATUS = (("traveling", "traveling"), ("No-travel", "No-travel"))
    ID_image = models.BinaryField(null=True,blank=True,editable=True)
    image = models.ImageField()
    car = models.CharField(choices=CARS, max_length=10)
    count_trip = models.PositiveIntegerField(default=0)
    status = models.CharField(choices=STATUS, max_length=11)
    
    def get_main_image(self):
        return b64encode(self.main_image).decode('utf-8')
    
    @staticmethod
    def compress_image(image,thumbnail_size=(400, 400)):
        im = Image.open(image)
        im_io = BytesIO()
        im = im.convert('RGB')
        if thumbnail_size:
            im.thumbnail(thumbnail_size)
        im.save(im_io, 'JPEG', quality=40)
        return im_io.getvalue()
    
    def delete(self,*args,delete_files=False,**kwargs):
        if delete_files:
            bucket.delete_object(self.car_image.name)
        return super().delete(*args,**kwargs)


class CustomerProfile(BaseProfile):
    pass
