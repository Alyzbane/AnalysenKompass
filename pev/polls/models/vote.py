from django.db import models
from django.contrib.auth.models import User
from . import Poll, Choice

from surveys.models import Survey

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_mean(self):
        pass
    
    def selected_choice(self):
        return self.choice
    
    def is_owner(self, user):
        return self.user == user

    def __str__(self):
        return f'{self.poll.text[:15]} - {self.choice.choice_text[:15]} - {self.user.username}'
