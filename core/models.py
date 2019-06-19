from django.db import models

# Create your models here.


class Stack(models.Model):
    name = models.CharField(max_length=100)

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

    def __str__(self):
        return self.prompt
