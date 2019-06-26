from django.db import models
from django.contrib.auth.models import User

## Safer, but more complex method
# from django.contrib.auth import get_user_model
# User = get_user_model()

# Create your models here.


class Stack(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Card(models.Model):
    prompt = models.TextField(
        verbose_name="Card prompt",
        help_text="This is what you will see on the front of the card.")
    answer = models.TextField(
        verbose_name="Card answer",
        help_text="This is what you will see on the back of the card.")
    stack = models.ForeignKey(to=Stack, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.prompt

    def times_correct(self, user=None):
        if user is None:
            return self.answer_records.filter(correct=True).count()
        if not user.is_authenticated:
            return None
        return self.answer_records.filter(user=user, correct=True).count()

    def times_incorrect(self, user=None):
        if user is None:
            return self.answer_records.filter(correct=False).count()
        if not user.is_authenticated:
            return None
        return self.answer_records.filter(user=user, correct=False).count()

    def record_result(self, correct, user):
        if user.is_authenticated:
            self.answer_records.create(correct=correct, user=user)
        else:
            self.answer_records.create(correct=correct)

        self.save()
        return self


class AnswerRecord(models.Model):
    """
    Record of whether the user answered the card correctly or incorrectly.
    """
    card = models.ForeignKey(to=Card,
                             on_delete=models.CASCADE,
                             related_name='answer_records')
    correct = models.BooleanField()
    answered_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
