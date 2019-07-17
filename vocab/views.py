from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.conf import settings


def vocab_quiz(request):
    return render(request, "vocab/quiz.html")


def random_word_json(request):
    got_defs = False
    while not got_defs:
        words_api_request = requests.get(
            'https://wordsapiv1.p.mashape.com/words/?random=true',
            headers={'X-Mashape-Key': settings.WORDS_API_KEY})
        word_data = words_api_request.json()
        if word_data.get('results') and word_data['results'][0].get(
                'definition'):
            got_defs = True

    response_data = {"word": word_data['word'], "definitions": []}

    for result in word_data['results']:
        if result.get("definition"):
            response_data["definitions"].append(result["definition"])

    return JsonResponse(response_data)
