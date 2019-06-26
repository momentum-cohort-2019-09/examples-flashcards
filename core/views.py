from django.shortcuts import render, redirect, get_object_or_404
from core.models import Stack, Card
from core.forms import StackForm, CardForm, CardResultsForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


def stack_list(request):
    """
    On GET - show all stacks.
    On POST - create a new stack.
    """
    if request.method == "POST" and request.user.is_authenticated:
        form = StackForm(data=request.POST)
        if form.is_valid():
            stack = form.save(commit=False)
            stack.owner = request.user
            stack.save()
            return redirect(to='stack-list')
    else:
        form = StackForm()

    if request.user.is_authenticated:
        my_stacks = Stack.objects.filter(owner=request.user)
        other_stacks = Stack.objects.exclude(owner=request.user)
    else:
        my_stacks = []
        other_stacks = Stack.objects.all()

    return render(request, 'core/stack_list.html', {
        "my_stacks": my_stacks,
        "other_stacks": other_stacks,
        "form": form
    })


def stack_detail(request, stack_pk):
    """
    View for /stacks/<stack_pk>
    Gets a stack and display all the cards in it.
    """
    stack = get_object_or_404(Stack, pk=stack_pk)
    return render(request, 'core/stack_detail.html', {
        "stack": stack,
        "card_count": stack.card_set.count(),
    })


def card_create(request, stack_pk):
    stack = get_object_or_404(Stack, pk=stack_pk)

    if request.method == "POST":
        form = CardForm(data=request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.stack = stack
            card.save()
            return redirect('stack-detail', stack_pk=stack.pk)
    else:
        form = CardForm()

    return render(request, 'core/card_create.html', {
        "stack": stack,
        "form": form
    })


def stack_quiz(request, stack_pk):
    """
    Show the user a random card from the chosen stack.
    """
    stack = get_object_or_404(Stack, pk=stack_pk)
    form = CardResultsForm()

    # TODO rewrite when we learn about aggregations
    # card = None
    # box_num = 0
    # while card is None and box_num <= 3:
    #     box_num += 1
    #     card = stack.card_set.filter(
    #         box_number=box_num).order_by('last_shown_at').first()

    # cards = stack.card_set_for_user(request.user)
    # card = cards.order_by('?')[0]

    card = stack.card_set.order_by('?').first()

    return render(
        request, 'core/stack_quiz.html', {
            "stack": stack,
            "card": card,
            "form": form,
            "times_correct": card.times_correct(request.user),
            "times_incorrect": card.times_incorrect(request.user),
        })


def card_results(request, card_pk):
    """
    View to submit correct/incorrect results for a card.
    """
    card = get_object_or_404(Card, pk=card_pk)
    form = CardResultsForm(request.POST)
    if form.is_valid():
        correct = form.cleaned_data['correct']
        card.record_result(correct, request.user)
    else:
        raise RuntimeError()
    return redirect(to='stack-quiz', stack_pk=card.stack.pk)
