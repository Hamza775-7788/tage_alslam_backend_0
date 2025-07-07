from django.db import models

# Create your models here.


class Government(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)
    government = models.ForeignKey(Government, on_delete=models.CASCADE, related_name='regions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='profile_image', blank=True, null=True)
    compny_name = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=254, blank=True,null=True)
    phone_number = models.CharField(max_length=15, blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    government = models.ForeignKey(Government, on_delete=models.SET_NULL, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
     # Store hashed passwords
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name