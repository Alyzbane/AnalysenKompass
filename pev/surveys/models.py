from django.db import models
from django.contrib.auth.models import User

class Survey(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_polls(self):
        return self.poll_set.all()
    def is_owner(self, user):
       return self.owner == user 
    def __str__(self) -> str:
        return self.title