from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

# Create your views here.




def  register(request):
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        emails = []
        emails.append(list(User.objects.filter(email=email)))
        
        if is_null(username):
            messages.error(request, 'Nome de Usuário Inválido.')
            return redirect('register')
        if is_null(password):
            messages.error(request, 'Senha Invalida.')
            return redirect('register')
        if password != confirmation:
            messages.error(request, 'As senhas precisam ser iguais.')
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Usuário já cadastrado.')
            return redirect('register')
        
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        messages.success(request, "Cadastro realizado com sucesso!")
        return redirect('login')
    else:
        auth.logout(request)
        return render(request, 'busers/register.html')

def login(request):
    if request.method == "GET":
        auth.logout(request)
        return render(request, 'busers/login.html')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
    if email == "" or password =="":
        messages.error(request, "Usuário ou senha inválidos!")
        return redirect('/login')
    if User.objects.filter(email=email).exists():
        name = User.objects.filter(email=email).values_list('username', flat=True)
        user = auth.authenticate(request, username=name[0], password=password)
        if user is not None:
            auth.login(request, user)
        return redirect('index')
    else:
        return render(request, 'busers/login.html')

def logout(request):
    auth.logout(request)
    #messages("Usuário Deslogado!")
    return redirect('login')


def is_null(field):
    return not field.strip()