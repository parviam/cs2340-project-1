from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, CustomErrorList
from django.shortcuts import redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')
def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
    if form.is_valid():
        form.save()
        return redirect('accounts.login')
    else:
        template_data['form'] = form
        return render(request, 'accounts/signup.html',
            {'template_data': template_data})
def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
        {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
        request,
        username = request.POST['username'],
        password = request.POST['password']
        )
    if user is None:
        template_data['error'] = 'The username or password is incorrect.'
        return render(request, 'accounts/login.html',
        {'template_data': template_data})
    else:
        auth_login(request, user)
        return redirect('home.index')
def reset(request):
    template_data = {}
    template_data['title'] = 'Reset Password'
    if request.method == 'GET':
        return render(request, 'accounts/reset.html',
        {'template_data': template_data})
    elif request.method == 'POST':
        if request.POST['pinky-promise'] != "I pinky promise this is my account.":
            user = None
        else:
            user = User.objects.get(username=request.POST['username'])
            user.set_password(request.POST['password'])
            user.save()
    if user is None:
        template_data['error'] = 'The username is incorrect.'
        return render(request, 'accounts/reset.html',
        {'template_data': template_data})
    else:
        auth_login(request, user)
        return redirect('home.index')