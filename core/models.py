from django.db import models

# Create your models here.


class Stack(models.Model):
    name = models.CharField(max_length=100)

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
    box_number = models.PositiveIntegerField(default=1)
    last_shown_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.prompt

    def times_correct(self):
        return self.answer_records.filter(correct=True).count()

    def times_incorrect(self):
        return self.answer_records.filter(correct=False).count()

    def record_result(self, correct):
        self.answer_records.create(correct=correct)
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
