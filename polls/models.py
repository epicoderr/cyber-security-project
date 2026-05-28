import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class AdminNote(models.Model):
    title = models.CharField(max_length=200)
    private_pin = models.CharField(max_length=50)
    # FIX: add these
    # def set_pin(self, raw_pin):
        # self.private_pin = make_password(raw_pin)

    # def check_pin(self, raw_pin):
        # return check_password(raw_pin, self.private_pin)

    def __str__(self):
        return self.title