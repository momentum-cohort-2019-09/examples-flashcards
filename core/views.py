from django.shortcuts import render, redirect, get_object_or_404
from core.models import Stack
from core.forms import StackForm, CardForm


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
        "cards": stack.card_set.all(),
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
