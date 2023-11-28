from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    birthdate = models.DateField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'