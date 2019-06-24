from django.shortcuts import render, redirect, get_object_or_404
from core.models import Stack, Card
from core.forms import StackForm, CardForm, CardResultsForm
from django.utils import timezone


def stack_list(request):
    if request.method == "POST":
        form = StackForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='stack-list')
    else:
        form = StackForm()

    stacks = Stack.objects.all()
    return render(request, 'core/stack_list.html', {
        "stacks": stacks,
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

    card = stack.card_set.filter(box_number=1).order_by('?').first()

    last_shown_at = card.last_shown_at
    card.last_shown_at = timezone.now()
    card.save()
    return render(request, 'core/stack_quiz.html', {
        "stack": stack,
        "card": card,
        "form": form,
        "last_shown_at": last_shown_at,
    })


def card_results(request, card_pk):
    """
    View to submit correct/incorrect results for a card.
    """
    card = get_object_or_404(Card, pk=card_pk)
    form = CardResultsForm(request.POST)
    if form.is_valid():
        correct = form.cleaned_data['correct']
        card.record_result(correct)
    else:
        raise RuntimeError()
    return redirect(to='stack-quiz', stack_pk=card.stack.pk)
