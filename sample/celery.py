
from __future__ import absolute_import

import os
import django

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE','sample.settings')

django.setup() #required in dj1.7 and above for app registry


app = Celery('sample')#instantiate our celery object, so that we have app running on celery
#celery is actually dependent upon its own application
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS) #looks for tasks.py file in all apps

