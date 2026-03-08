from django.shortcuts import render
from .forms import RegistrationForm #import the registration form we created in forms.py
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm #we will use the built in authentication form provided by django for login functionality.
from django.contrib import auth #we will use the built in authentication system provided by django to authenticate users during login and to log them out.

# Create your views here.
def home(request):
  return render(request, 'home.html')

def register(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, 'Registration successful.')
      return redirect('login')
    else:
      context = {
        'form': form,
      } #form by default will contain error messages for invalid fields, so we can just pass it to the template and display those errors there.
      return render(request, 'register.html', context)
  else:
    form = RegistrationForm()
    context = {
     'form': form,
    }
  return render(request, 'register.html', context)


# def login(request):
#   form = AuthenticationForm()

#   if request.method == 'POST':
#     form = AuthenticationForm(request, data=request.POST)

#     if form.is_valid():
#       username = form.cleaned_data['username']
#       password = form.cleaned_data['password']

#       user = auth.authenticate(username=username, password=password)

#       # 成功時の処理
#       if user is not None:
#         auth.login(request, user)
#         return redirect('home')
      
#     else:
#       messages.error(request, 'Invalid credentials. Please try again.')

#   # POST失敗時もここに来る
#   return render(request, 'login.html', {'form': form})

def login(request):
  if request.method == 'POST':
      form = AuthenticationForm(request, data=request.POST)

      if form.is_valid():
          user = form.get_user()
          auth.login(request, user)
          return redirect('home')

      # form.is_valid() が False のときはここに来る
      messages.error(request, 'Invalid credentials. Please try again.')
      return render(request, 'login.html', {'form': form})

  # GET
  form = AuthenticationForm()
  return render(request, 'login.html', {'form': form})


def logout(request):
  auth.logout(request)
  return redirect('home')
