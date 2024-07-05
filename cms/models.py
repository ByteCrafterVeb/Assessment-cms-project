from django.db import models
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Profile(models.Model):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('author', 'Author'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=6)

class Category(models.Model):
    name = models.CharField(max_length=50)

class Content(models.Model):
    title = models.CharField(max_length=30)
    body = models.TextField(max_length=300)
    summary = models.CharField(max_length=60)
    document = models.FileField(upload_to='documents/')
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

