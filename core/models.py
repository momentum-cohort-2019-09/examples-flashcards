from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, Count

## Safer, but more complex method
# from django.contrib.auth import get_user_model
# User = get_user_model()

# Create your models here.


class Stack(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)

    # def card_set_for_user(self, user):
    #     if not user.is_authenticated:
    #         return self.card_set.all()

    #     return self.card_set.annotate(
    #         times_correct=Count('answer_records',
    #                             filter=Q(answer_records__user=user,
    #                                      answer_records__correct=True)),
    #         times_incorrect=Count('answer_records',
    #                               filter=Q(answer_records__user=user,
    #                                        answer_records__correct=False)),
    #     )

    def __str__(self):
        return self.name


MIN_BOX_NUMBER = 1
MAX_BOX_NUMBER = 3


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

    def times_correct(self, user):
        if not user.is_authenticated:
            return None
        return self.answer_records.filter(user=user, correct=True).count()

    def times_incorrect(self, user):
        if not user.is_authenticated:
            return None
        return self.answer_records.filter(user=user, correct=False).count()

    def record_result(self, correct, user):
        if user.is_authenticated:
            self.answer_records.create(correct=correct, user=user)
        else:
            self.answer_records.create(correct=correct)

        # TODO this will not work now that we have multiple users
        if correct:
            self.box_number = min([MAX_BOX_NUMBER, self.box_number + 1])
        else:
            self.box_number = MIN_BOX_NUMBER
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
