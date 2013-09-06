from django.shortcuts import redirect, render

from niko.models import Vote

def dashboard(request):
    latest_poll_list = Vote.objects.all().order_by('-pub_date')
    context = {'latest_poll_list': latest_poll_list}
    return render(request, 'dashboard.html', context)

def save(request, mood):
    return redirect('dashboard')

def vote(request):
    return render(request, 'vote.html')
