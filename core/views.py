from django.shortcuts import render, redirect, get_object_or_404
from core.models import Stack


def stack_list(request):
    if request.method == "POST":

        new_stack_name = request.POST['stack_name']
        new_stack = Stack(name=new_stack_name)
        new_stack.save()
        return redirect(to='stack-list')

    stacks = Stack.objects.all()
    return render(request, 'core/stack_list.html', {"stacks": stacks})


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
