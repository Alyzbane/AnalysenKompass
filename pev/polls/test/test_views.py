from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from polls.models import Poll, Vote, Choice
from surveys.models import Survey