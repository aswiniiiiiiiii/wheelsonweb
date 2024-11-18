from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth import get_user_model
from django.shortcuts import render


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, is_staff=False, email=None):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, is_staff=is_staff, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, email=None):
        user = self.create_user(username, password=password, is_staff=True, email=email)
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(max_length=100,unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        related_query_name='user',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        related_query_name='user',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return self.username
    
class FuelType(models.Model):
    fuel = models.CharField(max_length=50)

    def __str__(self):
        return self.fuel
    
class District(models.Model):
    district = models.CharField(max_length=100 ,default="")

    def __str__(self):
        return self.district
    
class VehicleType(models.Model):
    type_name = models.CharField(max_length=100)

    def __str__(self):
        return self.type_name

class VehicleBrand(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Year(models.Model):
    year = models.PositiveIntegerField()

    def __str__(self):
        return str(self.year)
    
class OwnerType(models.Model):
    owner_type = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.owner_type
    
class GearType(models.Model):
    gear_type = models.CharField(max_length=100, default="" )

    def __str__(self):
        return self.gear_type
    
class SellVehicle(models.Model):
    seller = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=50)
    vehicle_name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE , default="")
    brand = models.ForeignKey(VehicleBrand, on_delete=models.CASCADE)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15)
    fuel_type = models.ForeignKey(FuelType, on_delete=models.CASCADE)
    km_driven = models.PositiveIntegerField(default=0)
    type_of_owner = models.ForeignKey(OwnerType, on_delete=models.CASCADE, default="", verbose_name="Type of Owner")
    type_of_gear = models.ForeignKey(GearType, on_delete=models.CASCADE, default="", verbose_name="Type of Gear") 
    location_link = models.URLField()
    image = models.ImageField(upload_to='vehicle_images/')
    image2 = models.ImageField(upload_to='vehicle_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='vehicle_images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='vehicle_images/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    emi_available = models.BooleanField(default=False, verbose_name="EMI Available") 
    description = models.TextField()

    def str(self):
        return f"{self.vehicle_name} - {self.registration_number}"
   
    
class RentVehicle(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='rented_vehicles')
    registration_number = models.CharField(max_length=50)
    district = models.ForeignKey(District, on_delete=models.CASCADE , default="")
    vehicle_name = models.CharField(max_length=100)
    brand = models.ForeignKey(VehicleBrand, on_delete=models.CASCADE)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    type_of_gear = models.ForeignKey(GearType, on_delete=models.CASCADE, default="", verbose_name="Type of Gear") 
    phone_number = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15)
    location_link = models.URLField()
    image = models.ImageField(upload_to='vehicle_images/')
    image2 = models.ImageField(upload_to='vehicle_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='vehicle_images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='vehicle_images/', blank=True, null=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    fuel_type = models.ForeignKey(FuelType, on_delete=models.CASCADE)
    km_driven = models.PositiveIntegerField(default=0)
    description = models.TextField()
   
    def __str__(self):
        return f"{self.vehicle_name} - {self.registration_number}"
    

class Feedback(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    feedback_text = models.TextField()
    rating = models.PositiveIntegerField(default=5, help_text="Enter a rating between 1 and 5")
    time = models.DateTimeField(auto_now_add=True)
    def adjusted_timestamp(self):
        return self.time + timedelta(hours=5, minutes=30)

    def __str__(self):
        return f"{self.user.username} - Rating: {self.rating}"
    
class QA(models.Model):
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return f" Question: {self.question[:20]}"

class Question(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    question_text = models.TextField()

    def __str__(self):
        return f"{self.user.username} - Question: {self.question_text}"
    
class QA_Buyer(models.Model):
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return f" Question: {self.question[:20]}"
    

    
