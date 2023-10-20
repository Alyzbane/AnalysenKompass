import datetime

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    question_text = models.CharField(max_length = 200)
    pub_date = models.DateTimeField("date published")

    def publish_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days = 1)

    def __str__(self):
        return self.question_text

