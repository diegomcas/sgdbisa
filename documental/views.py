from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError, DatabaseError, transaction
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Proyecto, Documento, Archivo
from calidad.models import Chequeo
from mensajes.models import Tique, Mensaje, MensajeDestinatarios, TiqueDestinatarios
from .forms import ProyectoForm, DocumentoForm, ArchivoForm, ObsDocForm
from .serializers import DocumentoSerializer
from .test_perms import list_proyectos, finalize_proyecto, view_proyecto, add_proyecto, update_proyecto
from .test_perms import list_documentos, view_documento, add_documento, update_documento
from .test_perms import delete_documento, revision_documento
from .test_perms import list_archivos, view_archivo, add_archivo, update_archivo
from .test_perms import delete_archivo, revision_archivo

def mensaje_destinatarios(mensaje, pk_proyecto):
    miembros = Proyecto.objects.get(pk=pk_proyecto).miembros.all()
    for miembro in miembros:
        # Tique Destinatario por cada miembro
        mensaje_dest = MensajeDestinatarios()
        mensaje_dest.miembro = miembro
        mensaje_dest.mensaje = mensaje
        mensaje_dest.save()

def emitir_mensaje(obj, msg):
    # Emitir mensaje
    mensaje = Mensaje()
    mensaje.mensaje = msg
    mensaje.fecha = timezone.now()
    mensaje.save()
    obj.mensaje.add(mensaje)
    # Mesaje a destinatarios
    mensaje_destinatarios(mensaje, obj.proyecto_id)

@user_passes_test(list_proyectos)
@login_required
def proyectos(request):
    """
    Presenta la lista completa de Proyectos existentes en el sistema
    """
    projs = Proyecto.objects.all().order_by('fecha', 'orden_trabajo')

    return render(
        request,
        'proyectos.html',
        {
            'proyectos': projs,
            'g_perms': request.user.get_all_permissions()
        }
    )

def tiques_open(proyecto):
    # Documentos->tiques
    tiques_doc = Tique.objects.filter(finalizado=False)
    tiques_doc = tiques_doc.filter(tiquesdoc__in=Documento.objects.filter(proyecto=proyecto))
    # Archivos->tiques
    tiques_file = Tique.objects.filter(finalizado=False)
    tiques_file = tiques_file.filter(tiquesarch__in=Archivo.objects.filter(proyecto=proyecto))

    return {'tiques_doc': tiques_doc, 'tiques_file': tiques_file}

@user_passes_test(finalize_proyecto)
@login_required
def finalizar_proyecto(request, primary_key):
    """
    Finaliza el proyecto actual.
    Asigna True a la propiedad 'finalizado' del Proyecto
    """
    proj = get_object_or_404(Proyecto, pk=primary_key)

    if request.method == "POST":
        if request.POST.get('confirma') == 'SI':
            proj.finalizado = True
            proj.save()

        return redirect('proyectos')

    return render(
        request,
        'finalizar_proyecto.html',
        {
            'tiques': tiques_open(proj),
            'proyecto': proj,
        }
    )


@user_passes_test(view_proyecto)
@user_passes_test(list_documentos)
@user_passes_test(list_archivos)
@login_required
def ver_proyecto(request, primary_key):
    """
    Muestra información del proyecto 'primary_key'
    y los documentos y archivos relacionados.
    """
    proyecto = get_object_or_404(Proyecto, pk=primary_key)

    return render(
        request,
        'proyecto_view.html',
        {
            'proyecto': proyecto,
            'g_perms': request.user.get_all_permissions()
        }
    )


@user_passes_test(add_proyecto)
@login_required
def nuevo_proyecto(request):
    """
    Crear un nuevo proyecto
    """
    if request.method == "POST":
        form = ProyectoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proyectos')
    else:
        form = ProyectoForm()

    return render(
        request,
        'proyecto.html',
        {'form': form}
    )


@user_passes_test(update_proyecto)
@login_required
def edita_proyecto(request, primary_key):
    """
    Editar el proyecto 'primary_key'
    """
    proj = get_object_or_404(Proyecto, pk=primary_key)

    if request.method == "POST":
        form = ProyectoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proyectos')
    else:
        form = ProyectoForm(instance=proj)

    return render(
        request,
        'proyecto.html',
        {'form': form}
    )


@user_passes_test(view_documento)
@login_required
def ver_documento(request, pk_proy, pk_doc):
    """
    Ver el documento 'pk_doc' preteneciente al proyecto 'pk_proy'
    """
    documento = get_object_or_404(Documento, pk=pk_doc)

    return render(
        request,
        'documento_view.html',
        {
            'documento': documento,
            'g_perms': request.user.get_all_permissions()
        }
    )


@user_passes_test(add_documento)
@login_required
def nuevo_documento(request, pk_proy):
    """
    Crear un documento preteneciente al proyecto 'pk_proy'
    """
    project = get_object_or_404(Proyecto, pk=pk_proy)

    if request.method == "POST":
        form = DocumentoForm(project, request.POST)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.proyecto = project
            doc = form.save()
            emitir_mensaje(doc, 'Se a creado el Documento')

            return redirect('ver_proyecto', primary_key=pk_proy)
    else:
        form = DocumentoForm(project)

    return render(
        request,
        'documento.html',
        {'form': form}
    )


@user_passes_test(update_documento)
@login_required
def edita_documento(request, pk_proy, pk_doc, pk_tique):
    """
    Modificar el documento 'pk_doc'
    """
    proj = get_object_or_404(Proyecto, pk=pk_proy)
    doc = get_object_or_404(Documento, pk=pk_doc)

    if request.method == "POST":
        form = DocumentoForm(proj, request.POST, instance=doc)
        if form.is_valid():
            doc = form.save()
            emitir_mensaje(doc, 'Se a modificado el Documento')
            if pk_tique > 0:
                tique = get_object_or_404(Tique, pk=pk_tique)
                tique.finalizado = True
                tique.fecha_finalización = timezone.now()
                tique.save()
                return redirect('index')
            else:
                return redirect('ver_proyecto', primary_key=pk_proy)
    else:
        form = DocumentoForm(proj, instance=doc)

    return render(
        request,
        'documento.html',
        {'form': form}
    )


@user_passes_test(update_documento)
@login_required
def observacion_documento(request, pk_proy, pk_doc, pk_tique):
    """
    Ejecuta versión reducida del formulario de modificación de documento
    relativo a observaciones
    """

    doc_observado = get_object_or_404(Documento, pk=pk_doc)
    tique = get_object_or_404(Tique, pk=pk_tique)

    if request.method == "POST":
        form = ObsDocForm(request.POST, instance=doc_observado)
        if form.is_valid():
            form.save()

            # Emitir mensaje
            emitir_mensaje(doc_observado, 'Se ha emitido una observación del documento.')

            # Finalizar Tique
            tique.finalizado = True
            tique.fecha_finalización = timezone.now()
            tique.save()
            return redirect('index')
    else:
        form = ObsDocForm(instance=doc_observado)

    return render(
        request,
        'documento_observacion.html',
        {
            'form': form,
            'tique': tique
        }
    )


@user_passes_test(revision_documento)
@login_required
def revision_documento(request, pk_proy, pk_doc, pk_tique):
    """
    Crea una revisión del documento 'pk_doc'
    """
    doc_a_revisionar = get_object_or_404(Documento, pk=pk_doc)

    if request.method == "POST":
        doc_revision = doc_a_revisionar.documento_reemplazado_por.get()
        form = DocumentoForm(doc_revision.proyecto, request.POST, instance=doc_revision)
        if form.is_valid():
            doc_revision = form.save()
            # Emitir mensaje
            emitir_mensaje(doc_revision, 'Se ha emitido una revisión del documento.')

            if pk_tique > 0:
                tique = get_object_or_404(Tique, pk=pk_tique)
                tique.finalizado = True
                tique.fecha_finalización = timezone.now()
                tique.save()
                doc_revision.tique_revision = tique
                doc_revision.save()
                # Tiques abiertos pertenecientes a doc_a_revisionar se eliminan
                doc_a_revisionar.tique.filter(finalizado=False).delete()
                return redirect('index')
            else:
                return redirect('ver_proyecto', primary_key=pk_proy)

    else:
        doc_revision = doc_a_revisionar.make_revision_doc()
        form = DocumentoForm(doc_revision.proyecto, instance=doc_revision)

    return render(
        request,
        'documento.html',
        {'form': form}
    )


@user_passes_test(revision_archivo)
@login_required
def revision_archivo(request, pk_proy, pk_file, pk_tique):
    """
    Crea una revisión del archivo 'pk_file'
    """
    file_a_revisionar = get_object_or_404(Archivo, pk=pk_file)
    if request.method == "POST":
        file_revision = file_a_revisionar.archivo_reemplazado_por.get()
        form = ArchivoForm(file_revision.proyecto, request.POST, instance=file_revision)
        if form.is_valid():
            file_revision = form.save()
            # Emitir mensaje
            emitir_mensaje(file_revision, 'Se ha emitido una revisión del archivo.')

            if pk_tique > 0:
                tique = get_object_or_404(Tique, pk=pk_tique)
                tique.finalizado = True
                tique.fecha_finalización = timezone.now()
                tique.save()
                file_revision.tique_revision = tique
                file_revision.save()
                # Tiques abiertos pertenecientes a file_a_revisionar se eliminan
                file_a_revisionar.tique.filter(finalizado=False).delete()
                return redirect('index')
            else:
                return redirect('ver_proyecto', primary_key=pk_proy)

    else:
        file_revision = file_a_revisionar.make_revision_file()
        form = ArchivoForm(file_revision.proyecto, instance=file_revision)

    return render(
        request,
        'archivo.html',
        {'form': form}
    )

@user_passes_test(delete_documento)
@login_required
def elimina_documento(request, pk_proy, pk_doc):
    """
    Renderiza una página de confirmación si no hay request.POST
    y request.POST['confirma'] es vacío o 'NO'
    Elimina el documento pk_doc.
    - Elimina los mensajes asociados al documento
        - Primero elimina las entradas a mensajes_destinatarios del documento
    - Elimina los tiques:
        - Primero elimina las entradas a tiques destinatarios
    - Elimina los elementos_espaciales asociados al documento
    """
    documento = get_object_or_404(Documento, pk=pk_doc)

    if request.method == "POST":
        if request.POST.get('confirma') == 'SI':
            # Borrar el documento
            doc_msgs = documento.mensaje.all()
            msg_dest = MensajeDestinatarios.objects.filter(mensaje__in=doc_msgs)
            doc_tqs = documento.tique.all()
            tqs_dest = TiqueDestinatarios.objects.filter(tique__in=doc_tqs)
            doc_ees = documento.espacial.all()
            chequeos = documento.chequeo_documento.all()

            try:
                with transaction.atomic():
                    chequeos.delete()
                    doc_ees.delete()
                    tqs_dest.delete()
                    doc_tqs.delete()
                    msg_dest.delete()
                    doc_msgs.delete()
                    documento.delete()
            except IntegrityError as ie:
                print(ie.values)

        # Redirect a ver_proyecto
        return redirect('ver_proyecto', primary_key=pk_proy)

    return render(
        request,
        'documento_delete.html',
        {'documento': documento}
    )


@user_passes_test(list_archivos)
@login_required
def archivos(request, pk_proy):
    """
    Presenta la lista completa de Archivos existentes en el sistema
    """
    files = Archivo.objects.all().order_by('nombre_archivo', 'revision')
    return render(
        request,
        'archivos.html',
        {
            'archivos': files,
            'g_perms': request.user.get_all_permissions()
        }
    )


@user_passes_test(view_archivo)
@login_required
def ver_archivo(request, pk_proy, pk_file):
    """
    Presenta toda la información de un archivo.
    """
    archivo = get_object_or_404(Archivo, pk=pk_file)

    return render(
        request,
        'archivo_view.html',
        {
            'archivo': archivo,
            'g_perms': request.user.get_all_permissions()
        }
    )


@user_passes_test(add_archivo)
@login_required
def nuevo_archivo(request, pk_proy):
    """
    Crear un archivo nuevo
    """
    project = get_object_or_404(Proyecto, pk=pk_proy)

    if request.method == "POST":
        form = ArchivoForm(project, request.POST)
        if form.is_valid():
            archivo = form.save(commit=False)
            archivo.proyecto = project
            file = form.save()
            emitir_mensaje(file, 'Se a creado el Archivo')
            return redirect('ver_proyecto', primary_key=pk_proy)
    else:
        form = ArchivoForm(project)

    return render(request, 'archivo.html', {'form': form})


@user_passes_test(update_archivo)
@login_required
def edita_archivo(request, pk_proy, pk_file, pk_tique):
    """
    Edita un archivo nuevo pk_file
    """
    project = get_object_or_404(Proyecto, pk=pk_proy)
    file = get_object_or_404(Archivo, pk=pk_file)

    if request.method == "POST":
        form = ArchivoForm(project, request.POST, instance=file)
        if form.is_valid():
            archivo = form.save(commit=False)
            archivo.proyecto = project
            file = form.save()
            emitir_mensaje(file, 'Se a modificado el Archivo')
            if pk_tique > 0:
                tique = get_object_or_404(Tique, pk=pk_tique)
                tique.finalizado = True
                tique.fecha_finalización = timezone.now()
                tique.save()
                return redirect('index')
            else:
                return redirect('ver_proyecto', primary_key=pk_proy)
    else:
        form = ArchivoForm(project, instance=file)

    return render(request, 'archivo.html', {'form': form})


@user_passes_test(delete_archivo)
@login_required
def elimina_archivo(request, pk_proy, pk_file):
    """
    Renderiza una página de confirmación si no hay request.POST
    y request.POST['confirma'] es vacío o 'NO'
    Elimina el archivo pk_file.
    - Elimina los mensajes asociados al archivo
        - Primero elimina las entradas a mensajes_destinatarios del archivo
    - Elimina los tiques:
        - Primero elimina las entradas a tiques destinatarios
    - Elimina los elementos_espaciales asociados al archivo
    """
    archivo = get_object_or_404(Archivo, pk=pk_file)

    if request.method == "POST":
        if request.POST.get('confirma') == 'SI':
            # Borrar el archivo
            file_msgs = archivo.mensaje.all()
            msg_dest = MensajeDestinatarios.objects.filter(mensaje__in=file_msgs)
            file_tqs = archivo.tique.all()
            tqs_dest = TiqueDestinatarios.objects.filter(tique__in=file_tqs)
            file_ees = archivo.espacial.all()

            try:
                with transaction.atomic():
                    file_ees.delete()
                    tqs_dest.delete()
                    file_tqs.delete()
                    msg_dest.delete()
                    file_msgs.delete()
                    archivo.delete()
            except IntegrityError as ie:
                print(ie.values)

        # Redirect a ver_proyecto
        return redirect('ver_proyecto', primary_key=pk_proy)

    return render(
        request,
        'archivo_delete.html',
        {'archivo': archivo}
    )


# ----------------------------------------------------------------------
# API REST VIEWs -------------------------------------------------------
# ----------------------------------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def find_docs(request, num_doc):
    """
    Retorna solo los documentos de numero num_doc en su ultima revisión
    """
    if request.method == 'GET':
        documentos = Documento.objects.filter(
            numero__contains=num_doc,
            documento_reemplazado_por=None
        )

        serializer = DocumentoSerializer(documentos, many=True)
        return Response(serializer.data)
