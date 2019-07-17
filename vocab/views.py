from django.shortcuts import render
from django.http import JsonResponse


def vocab_quiz(request):
    return render(request, "vocab/quiz.html")


def random_word_json(request):
    return JsonResponse({
        "word": "jam",
        "definitions": [
            "informal terms for a difficult situation",
            "deliberate radiation or reflection of electromagnetic energy for the purpose of disrupting enemy use of electronic devices or systems",
            "preserve of crushed fruit",
        ]
    })
