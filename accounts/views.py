from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if passwords does not match
        if password != password2:
            messages.error(request, 'Passwords do not match')
        # Check for new username
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'That username is taken')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'That email is being used')
        else:
            # Looks good
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            # Login after register
            #auth.login(request, user)
            #messages.success(request, 'You are now logged in')
            # return redirect('index')

            # redirect to login page to login for first time
            user.save()
            messages.success(
                request, 'You are now registered and can log in')
            return redirect('login')

        return redirect('register')
    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')


def dashboard(request):
    print(request.path)
    return render(request, 'accounts/dashboard.html')
