from sample.celery import app

from django.contrib.auth.models import User, Group

@app.task
def hello_world():
    print "Hello World"

@app.task
def update_user(user_id):
    try:
        g = Group.objects.get(name='Agent')
    except Group.DoesNotExist:
        pass
    else:
        g.user_set.add(User.objects.get(id=user_id))
        g.save()


@app.task
def test_celery():
    print "Its working!!"
