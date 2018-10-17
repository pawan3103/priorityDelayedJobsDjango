celery -A sample worker -l debug

celery -A sample beat -l debug # for periodic tasks



Celery is used for distribution of tasks which dont need to be done under normal request response cycle(asynchronous).
for example sending mail, uploading images and many more, for that we just need to start celery server.

pip install celery


It requires messaging agent to handling requests from external sources, which is reffered to as broker.

pip install celery[redis] -other then redis we can use rebbitmq

now we will add these brokerurl in settings

BROKER_URL = 'redis//127.0.0.1:6379/0' -o for first database.
BROKER_TRANSPORT = 'redis'

Here we are storing our tasks which need to be executed in queue.


Now, we will create our celery.py file where first we will export default settings

`os.environ.setdefault('DJANGO_SETTINGS_MODULE','sample.settings')`

app = Celery('sample') #sample is project name
#instantiate our celery object, so that we have app running on celer,#celery is actually dependent upon its own application
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS) #looks for tasks.py file in all apps

once these is done we can run celery in different terminal(worker) which will execute tasks from queue

`celery -A <project_name> worker -l debug`

here we are setting -l(log level to debug to get extra info to debug)



To deal with periodic tasks   celery has celery beat
so we need to install
`pip install django-celery`

add `djcelery` to installed apps


CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

now need to migrate since we have djcelery installed

celery -A sample beat -l debug --max-interval=10
- beat will look for periodic tasks



## Running multiple queues for Priority Tasks ##

- To run multiple queues we need to update the celery settings, where we define different queues and default queue.

#Configuration for Multiple Queues#

`from kombu import Queue, Exchange

CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('priority_tasks', Exchange('priority_tasks'), routing_key='priority_tasks'),
)
CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE = 'default'
CELERY_DEFAULT_ROUTING_KEY = 'default'
CELERY_ROUTES = {
    'sampleapp.tasks.hello_world': {'queue': 'default'},
    'sampleapp.tasks.test_celery': {'queue': 'priority_tasks'},
}
`

- Here we can route the tasks by default to different queues, like hello_world task can be queued in normal flow and test_celery task is queued to priority_tasks queue.
- Another way is providing the queue info in delay task, for example running  

`test_celery.apply_async(queue='priority_tasks')`

- Now, before that we need to run different workers for different queues.

`celery -A config worker -E -l INFO -n worker.default -Q default` and
`celery -A config worker -E -l INFO -n worker.priority_tasks -Q priority_tasks`
