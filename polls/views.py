from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from polls.forms import PollForm, Pollv2Form, QuestionForm
from polls.models import Poll, Pollv2, PollQ


# Create your views here.
def poll_list(request):
    polls = Pollv2.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'polls/poll_list.html', {'polls': polls})

def poll_vote(request, pk):
    poll = get_object_or_404(Pollv2, pk=pk)
    options = PollQ.objects.filter(poll=poll)
    if request.method == "POST":
        option = request.POST.get("option")
        option_object = get_object_or_404(PollQ, pk=int(option))
        option_object.votes += 1
        option_object.save()
        messages.add_message(request, messages.INFO, f"You voted for {option_object.description}")
        return redirect('poll_detailv2', poll.pk)

    return render(request, 'polls/poll_vote.html', {'poll': poll, 'options': options,})

@login_required()
def poll_delete(request, pk):
    this_poll = get_object_or_404(Pollv2, pk=pk)
    if request.user != this_poll.author and request.user.is_superuser is False:
        messages.add_message(request, messages.ERROR, "You can't do that.")
        return redirect('poll_list', pk=this_poll.pk)
    this_poll.delete()
    return redirect('poll_list')

def poll_createv2(request):
    if request.method == "POST":
        form = Pollv2Form(request.POST)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.author = request.user
            poll.published_date = timezone.now()
            poll.save()
            return redirect('poll_detailv2', pk=poll.pk)
    form = Pollv2Form()
    return render(request, 'polls/poll_new.html', {'form': form})

def poll_detailv2(request, pk):
    poll = get_object_or_404(Pollv2, pk=pk)
    options = PollQ.objects.filter(poll=poll)
    return render(request, 'polls/poll_detail.html', {'poll': poll, 'options':options})

def add_options(request, pk):
    poll = get_object_or_404(Pollv2, pk=pk)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            option = form.save(commit=False)
            option.poll = poll
            option.save()
            return redirect('poll_detailv2', pk=poll.pk)
    form = QuestionForm()
    return render(request, 'polls/poll_new.html', {'form': form})

def options_delete(request, pk):
    this_option = get_object_or_404(PollQ, pk=pk)
    poll = this_option.poll
    if request.user != poll.author and request.user.is_superuser is False:
        messages.add_message(request, messages.ERROR, "You can't do that.")
        return redirect('poll_list', pk=poll.pk)
    this_option.delete()
    return redirect('poll_detailv2', pk=poll.pk)

def poll_edit(request, pk):
    poll = get_object_or_404(Pollv2, pk=pk)
    if request.user != poll.author:
        messages.add_message(request, messages.ERROR, "You can't do that.")
        print(request.user.is_superuser)
        return redirect('poll_detail', pk=poll.pk)
    if request.method == "POST":
        form = Pollv2Form(request.POST, instance=poll)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.author = request.user
            poll.edit_date = timezone.now()
            poll.save()
            return redirect('poll_detailv2', pk=poll.pk)
    else:
        form = Pollv2Form(instance=poll)
    return render(request, 'polls/poll_new.html', {'form': form})