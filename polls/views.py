from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return HttpResponse("hallo thar!")

def detail(request, question_id):
	return HttpResponse("you're looking at %s" % question_id)

def results(request, question_id):
	response = "you're looking at result %s"
	return HttpResponse(response % question_id)

def vote(request, question_id):
	return HttpResponse("you're voting on %s" % question_id) 