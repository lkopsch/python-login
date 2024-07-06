from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home(request):
    return render(request, "autentication/index.html")

def signup(request):

    if request.method == "POST":
    
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Usuário já existe")
            return redirect('home')
        
        if User.objects.filter(email=email):
            messages.error(request, "Email já em uso")
            return redirect('home')
        
        if len(username)>15:
            messages.error(request, "Usuário precisa ter menos do que 15 caracteres! ")
            return redirect('home')
        
        if pass1 != pass2: 
            messages.error(request, "Senhas não são iguais!")
            return redirect('home')
            
        if not username.isalnum():
            messages.error(request, "O nome não pode conter simbolos, apenas letras e números!")
            return redirect('home')


        myuser = User.objects.create_user(username, email, pass2)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Usuário criado com sucesso!")


        return redirect('signin')

    return render(request, "autentication/signup.html")

def signin(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "autentication/index.html", {'fname': fname})

        else:
            messages.error(request, "Usuário ou senha incorretos!")
            return redirect('signin')


    return render(request, "autentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Deslogado!")
    return redirect('home')
