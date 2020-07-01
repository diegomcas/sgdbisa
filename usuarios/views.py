from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    """
    Esta vista responde a la ruta vacía (solo nombre de dominio)
    Si existe cookie de sesión devolvemos la portada.
    Si no, se redirecciona al login.
    """
    if request.user.is_authenticated:
        # devolvemos la portada
        return render(request, "usuarios/index.html")
    # redireccionamos al login
    return redirect('/login')

def login(request):
    """
    Presenta el la pantalla de Login al usuario
    """
    # Creamos el formulario de autenticación vacío
    form = AuthenticationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/')

    # Si llegamos al final renderizamos el formulario
    return render(request, "usuarios/login.html", {'form': form})

def logout(request):
    """
    Cierra sesión y redirecciona al Login
    """
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/')

@login_required
def change_password(request):
    """
    Permite cambiar el password a los usuarios
    """
    form = PasswordChangeForm(request.user)
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = PasswordChangeForm(request.user, data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Actualizamos
            form.save()
            return redirect('/')

    return render(request, "usuarios/change_password.html", {'form': form})
