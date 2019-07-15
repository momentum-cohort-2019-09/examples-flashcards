from django.shortcuts import get_object_or_404
from core.models import Stack
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def random_card(request, stack_pk):
    """
    Given a stack, return a random card for the current user in JSON.
    """
    stack = get_object_or_404(Stack, pk=stack_pk)
    card = stack.random_card_for_user(request.user)

    return JsonResponse({"card": card.to_dict()})
