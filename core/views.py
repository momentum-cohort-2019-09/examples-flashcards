from core.forms import CardForm, CardResultsForm, StackForm
from core.models import Card, Stack
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DetailView, CreateView


class StackListView(View):

    def get(self, request):
        form = StackForm()
        return self.render_template(request, form)

    def post(self, request):
        if request.user.is_authenticated:
            form = StackForm(data=request.POST)
            if form.is_valid():
                stack = form.save(commit=False)
                stack.owner = request.user
                stack.save()
                messages.success(
                    request,
                    f"Your stack '{stack.name}' was created successfully.")
                return redirect(to='stack-list')
        else:
            form = StackForm()

        return self.render_template(request, form)

    def render_template(self, request, form):
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


class StackDetailView(DetailView):
    model = Stack


@login_required
def stack_all_cards(request, stack_pk):
    stack = get_object_or_404(Stack, pk=stack_pk)

    valid_sorts = ['prompt', 'answer', 'created_at']

    if stack.owner != request.user:
        messages.warning(
            request,
            "You tried to look at all cards for a stack that you do not own.")
        return redirect('stack-detail', stack_pk=stack.pk)

    sort = request.GET.get('sort', default='prompt')
    if sort not in valid_sorts:
        sort = 'prompt'
    cards = stack.card_set.order_by(sort)

    return render(request, 'core/stack_all_cards.html', {
        "stack": stack,
        "cards": cards,
        "sort": sort,
        "valid_sorts": valid_sorts,
    })


@login_required
def card_create(request, stack_pk):
    stack = get_object_or_404(Stack, pk=stack_pk)

    if stack.owner != request.user:
        messages.warning(
            request, "You tried to add a card to a stack that you do not own.")
        return redirect('stack-detail', stack_pk=stack.pk)

    if request.method == "POST":
        form = CardForm(data=request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.stack = stack
            card.save()
            messages.success(request, "Your card was created successfully.")
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
    if not request.user.is_authenticated:
        return redirect(to='stack-quiz', stack_pk=card.stack.pk)

    form = CardResultsForm(request.POST)
    if form.is_valid():
        correct = form.cleaned_data['correct']
        card.record_result(correct, request.user)
    else:
        raise RuntimeError()
    return redirect(to='stack-quiz', stack_pk=card.stack.pk)
