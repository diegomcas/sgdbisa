from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Tique, TiqueDestinatarios
from .models import MensajeDestinatarios
from .forms import TiqueForm
from documental.models import Archivo, Documento, Proyecto

def add_tique(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para agregar tiques.
    """
    if 'mensajes.add_tique' in user.get_all_permissions():
        return True

    return False

def get_tique(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para agregar tiques.
    """
    if 'mensajes.get_tique' in user.get_all_permissions():
        return True

    return False

def change_tique(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para agregar tiques.
    """
    if 'mensajes.change_tique' in user.get_all_permissions():
        return True

    return False

def delete_tique(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para agregar tiques.
    """
    if 'mensajes.delete_tique' in user.get_all_permissions():
        return True

    return False

def tique_destinatario(tique, pk_proyecto):
    miembros = Proyecto.objects.get(pk=pk_proyecto).miembros.all()
    for miembro in miembros:
        # Tique Destinatario por cada miembro
        tique_dest = TiqueDestinatarios()
        tique_dest.miembro = miembro
        tique_dest.tique = tique
        tique_dest.save()

@user_passes_test(add_tique)
@login_required
def agrega_tique_arch(request, pk_proy, pk_file):
    """Cargar un tique a un archivo"""
    file = get_object_or_404(Archivo, pk=pk_file)

    if request.method == "POST":
        form = TiqueForm(request.POST)
        if form.is_valid():
            tique = form.save(commit=False)
            tique.fecha_emision = timezone.now()
            tique.finalizado = False
            tique.save()
            file.tique.add(tique)
            file.save()
            # miembros del proyecto
            tique_destinatario(tique, pk_proy)

            return redirect('ver_proyecto', primary_key=pk_proy)
    else:
        form = TiqueForm()

    return render(
        request,
        'proyecto.html',
        {
            'form': form,
            'titulo': file.__str__()
        }
    )

@user_passes_test(add_tique)
@login_required
def agrega_tique_doc(request, pk_proy, pk_doc):
    """Cargar un tique a un documento"""
    doc = get_object_or_404(Documento, pk=pk_doc)

    if request.method == "POST":
        form = TiqueForm(request.POST)
        if form.is_valid():
            tique = form.save(commit=False)
            tique.fecha_emision = timezone.now()
            tique.finalizado = False
            tique.save()
            doc.tique.add(tique)
            doc.save()
            # miembros del proyecto
            tique_destinatario(tique, pk_proy)

            return redirect('ver_proyecto', primary_key=pk_proy)
    else:
        form = TiqueForm()

    return render(
        request,
        'proyecto.html',
        {
            'form': form,
            'titulo': doc.__str__()
        }
    )

@user_passes_test(get_tique)
@login_required
def tomar_tique(request, pk_tique):
    """Asigna el tique pk_tique al usuario request.user"""
    tique = get_object_or_404(Tique, pk=pk_tique)
    tique.propietario = request.user
    tique.fecha_adquisicion = timezone.now()
    tique.save()
    return redirect('index')

@login_required
def marcar_leido(request, pk_msg):
    """Marcar el mensaje como leido por el usuario request.user"""
    msg_dest = MensajeDestinatarios.objects.get(mensaje_id=pk_msg, miembro=request.user)
    msg_dest.leido = True
    msg_dest.save()
    return redirect('index')

def tiques_info(proyecto):
    tiques = []
    # Documentos->tiques
    tiques_doc = Tique.objects.filter(tiquesdoc__in=Documento.objects.filter(proyecto=proyecto))
    tiques_doc = tiques_doc.order_by('-fecha_emision', '-fecha_adquisicion', '-fecha_finalización')
    # Archivos->tiques
    tiques_file = Tique.objects.filter(tiquesarch__in=Archivo.objects.filter(proyecto=proyecto))
    tiques_file = tiques_file.order_by('-fecha_emision', '-fecha_adquisicion', '-fecha_finalización')

    for tique in tiques_doc:
        tq = {}
        tq['pk'] = tique.pk
        tq['elemento'] = tique.tiquesdoc.get()
        tq['tipo'] = 'Documento'
        tq['descripcion'] = tique.descripcion
        tq['emision'] = tique.fecha_emision
        tq['adquisicion'] = tique.fecha_adquisicion
        tq['finalizacion'] = tique.fecha_finalización
        tq['finalizado'] = tique.finalizado
        tq['tt'] = tique.get_tipo_tique_display()
        tq['propietario'] = tique.propietario
        tiques.append(tq)

    for tique in tiques_file:
        tq = {}
        tq['pk'] = tique.pk
        tq['elemento'] = tique.tiquesarch.get()
        tq['tipo'] = 'Archivo'
        tq['descripcion'] = tique.descripcion
        tq['emision'] = tique.fecha_emision
        tq['adquisicion'] = tique.fecha_adquisicion
        tq['finalizacion'] = tique.fecha_finalización
        tq['finalizado'] = tique.finalizado
        tq['tt'] = tique.get_tipo_tique_display()
        tq['propietario'] = tique.propietario
        tiques.append(tq)

    return tiques

@user_passes_test(add_tique)
@login_required
def gestion_tiquet(request, pk_proy):
    """Presenta un listado de todos los tiques del proyecto"""
    proyecto = get_object_or_404(Proyecto, pk=pk_proy)

    return render(
        request,
        'gestion_tique.html',
        {
            'proyecto': proyecto,
            'tiques': tiques_info(proyecto),
            'g_perms': request.user.get_all_permissions()
        }
    )

@user_passes_test(delete_tique)
@login_required
def elimina_tique(request, pk_proy, pk_tique):
    """Elimina el tique pk_tique"""
    tique = get_object_or_404(Tique, pk=pk_tique)
    if not tique.finalizado:
        try:
            tq_obj = tique.tiquesdoc.all()
        except Exception:
            tq_obj = tique.tiquesarch.all()
        print(tq_obj)
        # Eliminar TiqueDestinatarios
        tique_dest = TiqueDestinatarios.objects.filter(tique=tique)
        tique_dest.delete()
        # Eliminar el tique
        tique.delete()
        print(tq_obj)

    return redirect('gestion_tiquet', pk_proy)


@user_passes_test(change_tique)
@login_required
def libera_tique(request, pk_proy, pk_tique):
    """Quita el propietario del tique pk_tique"""
    tique = get_object_or_404(Tique, pk=pk_tique)
    if not tique.finalizado:
        tique.propietario = None
        tique.fecha_adquisicion = None
        tique.save()

    return redirect('gestion_tiquet', pk_proy)
