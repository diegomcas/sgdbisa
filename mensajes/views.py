from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Tique, TiqueDestinatarios
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
