from django.shortcuts import get_object_or_404
from core.models import Stack, Card
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import json


def random_card(request, stack_pk):
    """
    Given a stack, return a random card for the current user in JSON.
    """
    stack = get_object_or_404(Stack, pk=stack_pk)
    card = stack.random_card_for_user(request.user)

    return JsonResponse({
        "card": {
            "pk": card.pk,
            "prompt": card.prompt,
            "answer": card.answer,
            "last_answered_at": card.last_answered_at,
            "answer_count": card.answer_count,
            "times_answered": card.times_answered,
            "times_correct": card.times_correct,
            "times_incorrect": card.times_incorrect,
        }
    })


@require_http_methods(['POST'])
def post_card_results(request, card_pk):
    """
    Given a JSON request stating whether the card was answered correctly or not,
    store that answer and reply.
    """
    card = get_object_or_404(Card, pk=card_pk)
    req_data = json.loads(request.body.decode("UTF-8"))
    card.record_result(req_data['correct'], request.user)
    return JsonResponse({"correct": req_data['correct']})
