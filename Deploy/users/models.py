from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

class AirQualityData(models.Model):
    pm25 = models.FloatField(blank=True, null=True)
    pm10 = models.FloatField(blank=True, null=True)
    no = models.FloatField(blank=True, null=True)
    no2 = models.FloatField(blank=True, null=True)
    nox = models.FloatField(blank=True, null=True)
    nh3 = models.FloatField(blank=True, null=True)
    co = models.FloatField(blank=True, null=True)
    so2 = models.FloatField(blank=True, null=True)
    o3 = models.FloatField(blank=True, null=True)
    benzene = models.FloatField(blank=True, null=True)
    toluene = models.FloatField(blank=True, null=True)
    xylene = models.FloatField(blank=True, null=True)
    aqi = models.FloatField(blank=True, null=True)
    label=models.CharField(max_length=200)
    
    def __str__(self):
        return f"Air Quality Data for {self.label}"
