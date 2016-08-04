import datetime

from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse 

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


def create_question(question_text, days):
	'''
	creates a question with inputted question text
	and pub date with offset inputted date - negative 
	dates for the past and positive for future
	'''
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionViewTests(TestCase):

	def test_index_view_with_no_questions(self):
		'''
		if no questions exist, appropriate message should be displayed
		'''
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls available")
		self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_index_view_with_a_past_question(self):
		'''
		questions with pub date in past shoulc be displayed
		on index page
		'''
		create_question(question_text="Past question", days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
		  response.context['latest_question_list'],
		  ['<Question: Past question>']
		)

	def test_index_view_with_a_future_question(self):
		'''
		questions with a pub_date in the future should not
		be displayed on the index page
		'''	
		create_question(question_text="Future question", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertContains(response, 'No polls available')
		self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_index_view_with_future_and_past_questions(self):
		'''
		if both future and past questions exists, 
		only past questions are shown 
		'''
		create_question(question_text="Past question", days=-30)
		create_question(question_text="Future question", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
		  response.context['latest_question_list'],
		  ['<Question: Past question>']
		)

	def test_index_view_with_multiple_past_questions(self):
		'''
		index page should display multiple questions 
		'''
		create_question(question_text="Past question 1", days=-30)
		create_question(question_text="Past question 2", days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
		  response.context['latest_question_list'],
		  ['<Question: Past question 1>', '<Question: Past question 2>']
		)


class QuestionIndexDetailTests(TestCase):

	def test_detail_view_with_future_question(self):
		'''
		detail view of an unpublished question 
		should return 404
		'''
		future_question = create_question(question_text="Future question", days=30)
		url = reverse('polls:detail', args=(future_question.id,))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)




