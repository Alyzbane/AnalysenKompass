from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
from django.db.models import Q
from . import Poll, Choice

from surveys.models import Survey

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
           models.Index(fields=['user']),
           models.Index(fields=['survey']),
           models.Index(fields=['poll', 'choice']),
        ]

    @classmethod
    def get_plot_dic(cls, poll_id, sex=None, birthdate=None):
        # Define all of the choices to be read for labels
        choices = Poll.objects.filter(pk=poll_id).values_list('choice__text', flat=True)

        # Use Q objects to dynamically construct the queryset with optional filters
        filter_conditions = Q(poll_id=poll_id)
        if birthdate:
            filter_conditions &= Q(user__profile__birthdate=birthdate)
        if sex:
            filter_conditions &= Q(user__profile__sex=sex)
            
        # Define the choices and its votes in the poll
        votes = cls.objects.filter(filter_conditions).values('choice__text').annotate(count=Count('choice'))

        # Define the easy lookup for the missing item in the votes
        vote_count_dict = {item['choice__text']: item['count'] for item in votes}

        data = [(choice, vote_count_dict.get(choice, 0)) for choice in choices]

        return data

    def get_choice_sets(self):
        return Choice.objects.filter()

    @classmethod
    def survey_complete(cls, user, survey_id):
        polls = Poll.objects.filter(survey_id=survey_id)
        user_votes = cls.objects.filter(user=user, poll__in=polls)
        return polls.count() == user_votes.count()

    def selected_choice(self):
        return self.choice

    def is_owner(self, user):
        return self.user == user

    def __str__(self):
        return f'{self.poll.text[:15]} - {self.choice.text[:15]} - {self.user.username}'
