import secrets

from django.db import models
from django.utils import timezone

from surveys.models import Survey

class Poll(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE) 
    text = models.TextField(max_length=255)
    pub_date = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    ### Start of navigation data helper
    ### Defines the data for navigation in the polls/partials/navigation.html
    @classmethod
    def get_next_poll(cls, survey_id, poll_id):
        try:
            next_poll = cls.objects.filter(survey_id=survey_id).filter(id__gt=poll_id).order_by('id')[0]
            return next_poll.id
        except IndexError:
            return None
    @classmethod
    def get_previous_poll(cls, survey_id, poll_id):
        try:
            previous_poll = cls.objects.filter(survey_id=survey_id).filter(id__lt=poll_id).order_by('-id')[0]
            return previous_poll.id
        except IndexError:
            return None

    def has_choices(self):
        return self.choice_set.exists()

    def is_owner(self, user):
        return self.survey.owner == user
    def user_can_vote(self, user):
        """ 
        Return False if user already voted
        """
        user_votes = user.vote_set.all()
        qs = user_votes.filter(poll=self)
        if qs.exists():
            return False
        return True

    @property
    def get_vote_count(self):
        return self.vote_set.count()
    
    @property
    def has_votes(self):
        return self.vote_set.exists()

    def __str__(self):
       return self.text