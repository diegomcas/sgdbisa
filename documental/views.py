from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Proyecto, Documento, Archivo
from calidad.models import Chequeo
from .forms import ProyectoForm, DocumentoForm, ArchivoForm
from .test_perms import list_proyectos, finalize_proyecto, view_proyecto, add_proyecto, update_proyecto
from .test_perms import list_documentos, view_documento, add_documento, update_documento
from .test_perms import delete_documento, revision_documento
from .test_perms import list_archivos, view_archivo, add_archivo, update_archivo
from .test_perms import delete_archivo, revision_archivo

@user_passes_test(list_proyectos)
@login_required
def proyectos(request):
    """
    Presenta la lista completa de Proyectos existentes en el sistema
    """
    projs = Proyecto.objects.all().order_by('fecha')
    return render(
        request,
        'proyectos.html',
        {
            'proyectos': projs,
            'g_perms': request.user.get_all_permissions()
        }
    )


@user_passes_test(finalize_proyecto)
@login_required
def finalizar_proyecto(request, primary_key):
    """
    Finaliza el proyecto actual.
    Asigna True a la propiedad 'finalizado' del Proyecto
    """
    proj = get_object_or_404(Proyecto, pk=primary_key)
    # ToDo: verificar que no existan tiques abiertos!!!
    return render(
        request,
        'finalizar_proyecto.html',
        {
            'proyecto': proj,
            'g_perms': request.user.get_all_permissions()
        }
    )


@user_passes_test(view_proyecto)
@user_passes_test(list_documentos)
@user_passes_test(list_archivos)
@login_required
def ver_proyecto(request, primary_key):
    """
    Muestra información del proyecto 'primary_key'
    y los documentos relacionados.
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
            form.save()
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
def edita_documento(request, pk_proy, pk_doc):
    """
    Modificar el documento 'pk_doc'
    """
    proj = get_object_or_404(Proyecto, pk=pk_proy)
    doc = get_object_or_404(Documento, pk=pk_doc)

    if request.method == "POST":
        form = DocumentoForm(proj, request.POST, instance=doc)
        if form.is_valid():
            form.save()
            return redirect('ver_proyecto', primary_key=pk_proy)
    else:
        form = DocumentoForm(proj, instance=doc)

    return render(
        request,
        'documento.html',
        {'form': form}
    )


@user_passes_test(revision_documento)
@login_required
def revision_documento(request, pk_proy, pk_doc):
    """
    Crea una revisión del documento 'pk_doc'
    """
    doc = get_object_or_404(Documento, pk=pk_doc)


@user_passes_test(delete_documento)
@login_required
def elimina_documento(request):
    pass


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
            form.save()
            return redirect('ver_proyecto', primary_key=pk_proy)
    else:
        form = ArchivoForm(project)

    return render(request, 'archivo.html', {'form': form})


@user_passes_test(update_archivo)
@login_required
def edita_archivo(request, pk_proy, pk_file):
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
            form.save()
            return redirect('ver_proyecto', primary_key=pk_proy)
    else:
        form = ArchivoForm(project, instance=file)

    return render(request, 'archivo.html', {'form': form})


@user_passes_test(delete_archivo)
@login_required
def elimina_archivo(request, pk_proy, pk_file):
    pass
