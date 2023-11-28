from django.db import models
from django.db.models import Count, Q
from django.contrib.auth.models import User
from . import Poll, Choice

from surveys.models import Survey

from datetime import date, timedelta

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
    def get_plot_dict(cls, poll_id, age_range=None, sex=None):
        filter_conditions = cls._build_filter_conditions(poll_id, age_range, sex)
        choices = cls._get_choices(poll_id)
        votes = cls._get_votes(filter_conditions)
        data = cls._calculate_plot_data(choices, votes)
        return data

    @classmethod
    def _build_filter_conditions(cls, poll_id, age_range, sex):
        filter_conditions = Q(poll_id=poll_id)

        if age_range:
            min_birthdate = date.today() - timedelta(days=(365 * age_range))
            filter_conditions &= Q(user__profile__birthdate__lte=min_birthdate)

        if sex:
            filter_conditions &= Q(user__profile__sex=sex)

        return filter_conditions

    @classmethod
    def _get_choices(cls, poll_id):
        choices = Poll.objects.filter(pk=poll_id).values_list('choice__text', flat=True)
        return choices

    @classmethod
    def _get_votes(cls, filter_conditions):
        votes = cls.objects.filter(filter_conditions).values('choice__text').annotate(count=Count('choice'))
        return {item['choice__text']: item['count'] for item in votes}

    @classmethod
    def _calculate_plot_data(cls, choices, votes):
        data = [(choice, votes.get(choice, 0)) for choice in choices]
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
