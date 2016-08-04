import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question 

class QuestionMethodTests(TestCase):

	def test_was_published_recently_with_recent_question(self):

		'''
		should return true for any question newer than 1 day
		'''
		time = timezone.now() - datetime.timedelta(hours=1)
		recent_question = Question(pub_date=time)
		self.assertEqual(recent_question.was_published_recently(), True)


	def test_was_published_recently_with_future_question(self):
		'''
		tests that test_was_published_recently returns
		false for questions with pub_date in the future
		'''
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertEqual(future_question.was_published_recently(), False)

	def test_was_published_recently_with_old_question(self):
		'''
		should return false for any question older than 1 day
		'''
		time = timezone.now() - datetime.timedelta(days=30)
		old_question = Question(pub_date=time)
		self.assertEqual(old_question.was_published_recently(), False)