# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from sampleapp.tasks import test_celery, hello_world

def home(request):
    hello_world.apply_async() # Will run it in default queue
    test_celery.apply_async(queue='priority_tasks') # Will run it in priority_tasks queue.
    return HttpResponse("Celery Demo!!")