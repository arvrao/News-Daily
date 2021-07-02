from django.shortcuts import render, redirect
# import login
from django.contrib.auth import login
# from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrationForm
# django default form for creating user

def main(request):
    return render(request, 'core/main.html')

def signUp(request):
    if request.method=="POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request,user)

            
            return redirect('/')

    else:
        form = RegistrationForm()

    return render(request,'core/signup.html', {'form':form})