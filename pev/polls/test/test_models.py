from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from polls.models import Poll, Vote, Choice
from surveys.models import Survey


class PollModelTest(TestCase):
    def test_poll_creation(self):
        """ 
        Create a poll from User side
        """
        user = User.objects.create_user('john')
        poll = Poll.objects.create(
            owner=user,  # Replace with your user ID
            text="Test Poll"
        )
        poll.save()

        # Check if the poll was saved to the database
        saved_poll = Poll.objects.get(pk=poll.pk)
        self.assertEqual(saved_poll.text, "Test Poll")

    def test_choices_creation(self):
        """
        Create a choices from the poll created
        """

        user = User.objects.create_user('john')
        poll = Poll.objects.create(
            owner=user,  # Replace with your user ID
            text="Test Poll with Choices"
        )

        # Create 5 test choice objects for the poll
        choices = []
        for i in range(1, 6):
            text = f"Test Choice {i}"
            choice = Choice.objects.create(
                poll=poll,
                text=text
            )
            choice.save()
            choices.append(choice)

        # Check if the choices were saved to the database
        saved_choices = Choice.objects.filter(poll=poll)
        self.assertEqual(saved_choices.count(), 5)

        # Check the text of each choice
        for i, saved_choice in enumerate(saved_choices):
            self.assertEqual(saved_choice.text, f"Test Choice {i + 1}")


class VoteModelTest(TestCase):

    def test_user_can_vote(self):
        """
        Check User voting permission
        """
        user = User.objects.create_user('john')
        poll = Poll.objects.create(owner=user)
        self.assertTrue(poll.user_can_vote(user))

        choice = poll.choice_set.create(text='pizza')
        Vote.objects.create(user=user, poll=poll, choice=choice)
        self.assertFalse(poll.user_can_vote(user))

    def test_vote_deleted_by_poll(self):
        """
        Delete the vote once the survey is deleted too
        """

        user = User.objects.create_user('wick')
        survey = Survey.objects.create(owner=user, title="test")
        self.assertTrue(survey.owner == user.username)
