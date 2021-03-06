from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group
from .forms import SignUpForm


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            Group.objects.get(name='Students').user_set.add(user)
            login(request, user)
            return redirect('moodle:index')
    else:
        form = SignUpForm()
    return render(request, 'authentication/register.html', {'form': form})
