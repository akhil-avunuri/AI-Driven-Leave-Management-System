from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to the admin_role index page
        else:
            messages.error(request, "Invalid email or password!")
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def pass_recovery(request):
    return render(request, 'pass_recovery.html')

def pages_404(request):
    return render(request, 'pages-404.html')