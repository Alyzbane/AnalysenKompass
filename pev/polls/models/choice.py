from django.db import models

from . import Poll

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_owner(self, user):
        return self.poll.survey.owner == user
    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def __str__(self):
        return f"{self.text[:25]}"
