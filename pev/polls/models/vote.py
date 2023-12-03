from django.db import models
from django.db.models import Count, Q
from django.contrib.auth.models import User
from . import Poll, Choice

from surveys.models import Survey

from datetime import date, timedelta

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    survey = models.ForeignKey(Survey, on_delete=models.SET_NULL, null=True)
    poll = models.ForeignKey(Poll, on_delete=models.SET_NULL, null=True)
    choice = models.ForeignKey(Choice, on_delete=models.SET_NULL, null=True)
    original_choice_text = models.CharField(max_length=255, blank=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
           models.Index(fields=['user']),
           models.Index(fields=['survey']),
           models.Index(fields=['poll', 'choice']),
        ]

    @classmethod
    def get_plot_dict(cls, poll_id, min_age=None, max_age=None, sex=None):
        filter_conditions = cls._build_filter_conditions(poll_id, min_age, max_age, sex)
        choices = cls._get_choices(poll_id)
        votes = cls._get_votes(filter_conditions)
        data = cls._calculate_plot_data(choices, votes)
        return data

    @classmethod
    def _build_filter_conditions(cls, poll_id, min_age=None, max_age=None, sex=None):
        filter_conditions = Q(poll_id=poll_id)

        if min_age is not None:
            min_birthdate = date.today() - timedelta(days=(365 * min_age))
            filter_conditions &= Q(user__profile__birthdate__lte=min_birthdate)

        if max_age is not None:
            max_birthdate = date.today() - timedelta(days=(365 * max_age))
            filter_conditions &= Q(user__profile__birthdate__gte=max_birthdate)

        if sex is not None:
            filter_conditions &= Q(user__profile__sex=sex)

        return filter_conditions

    @classmethod
    def _get_choices(cls, poll_id):
        choices = Choice.objects.filter(poll_id=poll_id).values_list('text', flat=True).distinct()
        return choices

    @classmethod
    def _get_votes(cls, filter_conditions):
        votes = cls.objects.filter(filter_conditions).values('original_choice_text').annotate(count=Count('original_choice_text'))
        return {item['original_choice_text']: item['count'] for item in votes}

    @classmethod
    def _calculate_plot_data(cls, choices, votes):
        data = [(choice, votes.get(choice, 0)) for choice in choices]

        for original_choice_text in votes.keys():
            if original_choice_text not in choices:
                data.append((original_choice_text, votes[original_choice_text]))

        return data

    @classmethod
    def survey_complete(cls, user, survey_id):
        polls = Poll.objects.filter(survey_id=survey_id)
        user_votes = cls.objects.filter(user=user, poll__in=polls)
        return polls.count() == user_votes.count()
    
    # override the save method for original choice
    def save(self, *args, **kwargs):
        if not self.original_choice_text:
            self.original_choice_text = self.choice.text
        super().save(*args, **kwargs)

    def selected_choice(self):
        return self.choice

    def is_owner(self, user):
        return self.user == user

    def __str__(self):
        return f'{self.original_choice_text[:15]}'
