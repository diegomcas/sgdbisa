from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.contrib.auth.decorators import login_required
from mensajes.models import Mensaje, Tique, MensajeDestinatarios, TiqueDestinatarios


def tiques_user_info(prop):
    tiques = []
    tiques_user = Tique.objects.filter(propietario=prop, finalizado=False)
    tiques_user = tiques_user.order_by('fecha_emision').order_by('fecha_adquisicion')
    for tq in tiques_user:
        tique = {}
        tique['pk'] = tq.pk
        tique['descripcion'] = tq.descripcion
        tique['fecha_emision'] = tq.fecha_emision
        tique['fecha_adquisicion'] = tq.fecha_adquisicion
        tique['tipo'] = tq.tipo_tique
        tique['tipo_text'] = tq.get_tipo_tique_display()
        # Objeto al que refiere el tique
        try:
            tq_obj = tq.tiquesdoc.get()
            tique['tipo_obj'] = 'Documento'
        except Exception:
            tq_obj = tq.tiquesarch.get()
            tique['tipo_obj'] = 'Archivo'

        tique['proyecto_pk'] = tq_obj.proyecto.pk
        tique['proyecto_ot'] = tq_obj.proyecto.__str__()
        tique['obj_pk'] = tq_obj.pk
        tique['obj_name'] = tq_obj.__str__()

        tiques.append(tique)

    return tiques

def tiques_abiertos_info(usuario):
    tiques = []
    tiquesdest_abiertos = TiqueDestinatarios.objects.filter(miembro=usuario)
    tiquesdest_abiertos = tiquesdest_abiertos.filter(tique__propietario__isnull=True)
    tiquesdest_abiertos = tiquesdest_abiertos.order_by('tique__fecha_emision')
    for tqdest in tiquesdest_abiertos:
        tique = {}
        tq = tqdest.tique
        tique['pk'] = tq.pk
        tique['descripcion'] = tq.descripcion
        tique['fecha_emision'] = tq.fecha_emision
        tique['fecha_adquisicion'] = tq.fecha_adquisicion
        tique['tipo'] = tq.tipo_tique
        tique['tipo_text'] = tq.get_tipo_tique_display()
        # Objeto al que refiere el tique
        try:
            tq_obj = tq.tiquesdoc.get()
            tique['tipo_obj'] = 'Documento'
        except Exception:
            tq_obj = tq.tiquesarch.get()
            tique['tipo_obj'] = 'Archivo'

        tique['proyecto_pk'] = tq_obj.proyecto.pk
        tique['proyecto_ot'] = tq_obj.proyecto.__str__()
        tique['obj_pk'] = tq_obj.pk
        tique['obj_name'] = tq_obj.__str__()

        tiques.append(tique)

    return tiques

def mensajes_info(usuario):
    # print(f'usuario:{usuario}')
    mensajes = []
    mensajes_dest = MensajeDestinatarios.objects.filter(miembro=usuario, leido=False)
    mensajes_dest = mensajes_dest.order_by('mensaje__fecha')
    print(mensajes_dest)
    for mensaje_dest in mensajes_dest:
        print(mensaje_dest.pk)
        print(mensaje_dest.mensaje)
        print(mensaje_dest.mensaje.mensaje)
        msg = mensaje_dest.mensaje
        mensaje = {}
        mensaje['pk'] = msg.pk
        mensaje['mensaje'] = msg.mensaje
        mensaje['fecha'] = msg.fecha
        try:
            msg_obj = msg.mensajesdoc.get()
            mensaje['tipo_obj'] = 'Documento'
        except Exception:
            msg_obj = msg.mensajesarch.get()
            mensaje['tipo_obj'] = 'Archivo'

        mensaje['proyecto_pk'] = msg_obj.proyecto.pk
        mensaje['proyecto_ot'] = msg_obj.proyecto.__str__()
        mensaje['obj_pk'] = msg_obj.pk
        mensaje['obj_name'] = msg_obj.__str__()

        mensajes.append(mensaje)

    return mensajes


def index(request):
    """
    Esta vista responde a la ruta vacía (solo nombre de dominio)
    Si existe cookie de sesión devolvemos la portada.
    Si no, se redirecciona al login.
    """
    if request.user.is_authenticated:
        # Tiques tomados por el usuario
        tiques_user = tiques_user_info(request.user)
        # print(tiques_user)
        # Todos los Mensajes del usuario
        mensajes = mensajes_info(request.user)
        # Todos los Tiques del Usuario menos los que tienen propietarios
        tiques_abiertos = tiques_abiertos_info(request.user)
        # print(tiques_abiertos)

        # devolvemos la portada
        return render(
            request,
            "usuarios/index.html",
            {
                'tiques_user': tiques_user,
                'mensajes': mensajes,
                'tiques_abiertos': tiques_abiertos,
            }
        )
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
