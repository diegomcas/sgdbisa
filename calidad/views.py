from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import ListaChequeo, TipoChequeo, Chequeo
from documental.models import Proyecto, Documento
from .serializers import DocumentoChequeoSerializer, ChequeoRealizadoSerializer
from .forms import ListaChequeoForm, TipoChequeoForm
from .test_perms import list_listas_chequeo, view_lista_chequeo, add_lista_chequeo
from .test_perms import update_lista_chequeo, delete_lista_chequeo
from .test_perms import list_tipos_chequeo, view_tipo_chequeo, add_tipo_chequeo
from .test_perms import update_tipo_chequeo, delete_tipo_chequeo
from .test_perms import add_chequeo, change_chequeo, delete_chequeo


@user_passes_test(list_listas_chequeo)
@login_required
def listas_chequeo(request):
    """
    Lista todas las listas de chequeo existentes en el sistema
    """
    lst_chequeo = ListaChequeo.objects.all().order_by('area')
    return render(
        request,
        'listas_chequeo.html',
        {
            'lst_chequeo': lst_chequeo,
            'g_perms': request.user.get_all_permissions()
        }
    )


@user_passes_test(view_lista_chequeo)
@login_required
def ver_lista_chequeo(request, pk_lc):
    """
    Muestra una lista de chequeo y los chequeos que contiene
    """
    lst_chequeo = get_object_or_404(ListaChequeo, pk=pk_lc)
    # tipos_chequeo = lst_chequeo.tipos_chequeo.all()
    return render(
        request,
        'lista_chequeo_view.html',
        {
            'lst_chequeo': lst_chequeo,
            # 'tipos_chequeo': tipos_chequeo,
            'g_perms': request.user.get_all_permissions()
        }
    )


@user_passes_test(add_lista_chequeo)
@login_required
def nueva_lista_chequeo(request):
    """
    Crear una nueva lista de chequeo
    opcionalmente agregarle tipos_chequeo
    """
    if request.method == "POST":
        form = ListaChequeoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listas_chequeo')
    else:
        form = ListaChequeoForm()

    return render(request, 'lista_chequeo.html', {'form': form})


@user_passes_test(update_lista_chequeo)
@login_required
def edita_lista_chequeo(request, pk_lc):
    """
    Edita una lista de chequeo
    opcionalmente agregarle tipos_chequeo
    """
    lst_chk = get_object_or_404(ListaChequeo, pk=pk_lc)

    if request.method == "POST":
        form = ListaChequeoForm(request.POST, instance=lst_chk)
        if form.is_valid():
            form.save()
            return redirect('listas_chequeo')
    else:
        form = ListaChequeoForm(instance=lst_chk)

    return render(request, 'lista_chequeo.html', {'form': form})


@user_passes_test(delete_lista_chequeo)
@login_required
def elimina_lista_chequeo(request, pk_lc):
    """
    Elimina una lista de chequeo
    Solo elimina la lista, no los tipos que incluye
    """
    lista_chequeo = get_object_or_404(ListaChequeo, pk=pk_lc)

    if request.method == "POST":
        acepta = (request.POST.get('acepta'))
        if acepta == 'LISTA':
            lista_chequeo.delete()
        if acepta == 'TODO':
            for tipo_chequeo in lista_chequeo.tipos_chequeo.all():
                if tipo_chequeo.tipo_chequeo.all().count() == 0:
                    tipo_chequeo.delete()
                    lista_chequeo.delete()

        return redirect('listas_chequeo')

    return render(
        request,
        'lista_chequeo_delete.html',
        {
            'lista_chequeo': lista_chequeo,
            'g_perms': request.user.get_all_permissions()
        }
    )


@user_passes_test(list_tipos_chequeo)
@login_required
def tipos_chequeo(request):
    """
    Lista todas los tipos de chequeo existentes en el sistema
    """
    tipos_chequeo = TipoChequeo.objects.all().order_by('nombre')
    return render(
        request,
        'tipos_chequeo.html',
        {
            'tipos_chequeo': tipos_chequeo,
            'g_perms': request.user.get_all_permissions()
        }
    )


@user_passes_test(view_tipo_chequeo)
@login_required
def ver_tipo_chequeo(request, pk_tc):
    """
    Muestra la información completa de un tipo de chequeo
    """
    # print(request.headers['referer'])
    tipo_chequeo = get_object_or_404(TipoChequeo, pk=pk_tc)
    return render(
        request,
        'tipo_chequeo_view.html',
        {
            'tipo_chequeo': tipo_chequeo,
            'g_perms': request.user.get_all_permissions()
        }
    )


@user_passes_test(add_tipo_chequeo)
@login_required
def nuevo_tipo_chequeo(request):
    """
    Crear un nuevo tipo de chequeo
    opcionalmente agregarlo a listas_chequeo
    """
    if request.method == "POST":
        form = TipoChequeoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tipos_chequeo')
    else:
        form = TipoChequeoForm()

    return render(request, 'tipo_chequeo.html', {'form': form})


@user_passes_test(update_tipo_chequeo)
@login_required
def edita_tipo_chequeo(request, pk_tc):
    """
    Modificar un tipo de chequeo
    opcionalmente agregarlo a listas_chequeo
    """
    tipo_chequeo = get_object_or_404(TipoChequeo, pk=pk_tc)

    if request.method == "POST":
        form = TipoChequeoForm(request.POST, instance=tipo_chequeo)
        if form.is_valid():
            form.save()
            return redirect('tipos_chequeo')
    else:
        form = TipoChequeoForm(instance=tipo_chequeo)

    return render(request, 'tipo_chequeo.html', {'form': form})


@user_passes_test(delete_tipo_chequeo)
@login_required
def elimina_tipo_chequeo(request, pk_tc):
    """
    Elimina un tipo de chequeo solo si no está referenciado por un Chequeo
    """
    tipo_chequeo = get_object_or_404(TipoChequeo, pk=pk_tc)

    if request.method == "POST":
        acepta = request.POST.get('acepta')
        if acepta == 'SI':
            tipo_chequeo.delete()

        return redirect('tipos_chequeo')

    return render(
        request,
        'tipo_chequeo_delete.html',
        {
            'tipo_chequeo': tipo_chequeo,
            'g_perms': request.user.get_all_permissions()
        }
    )


@user_passes_test(add_chequeo)
@login_required
def agrega_chequeo(request, pk_proy, pk_doc):
    """
    Agrega chequeos a un documento por medio de una lista de chequeo
    """
    doc = get_object_or_404(Documento, pk=pk_doc)
    listas_chequeo = ListaChequeo.objects.all()
    chequeos_doc = doc.chequeo_documento.all()
    # chequeos_doc = Chequeo.objects.filter(documento__pk=pk_doc)

    if request.method == "POST":
        id_listas_chequeo_sel = request.POST.getlist('listachequeo', '')
        for id_chk in id_listas_chequeo_sel:
            lista_chequeo = ListaChequeo.objects.get(pk=id_chk)
            tipos_chequeo_en_lista = lista_chequeo.tipos_chequeo.all()
            tipos_chequeos_en_doc = [
                tchk_doc.tipo_chequeo for tchk_doc in chequeos_doc
            ]
            for tcl in tipos_chequeo_en_lista:
                if tcl not in tipos_chequeos_en_doc:
                    # Creo un objeto Chequeo, le agrego el documento y lo guardo
                    chequeo_doc = Chequeo(
                        documento=doc,
                        tipo_chequeo=tcl,
                        verificado=False,
                        aplica=True,
                        verificado_por=None,
                    )
                    chequeo_doc.save()

        chequeos_doc = Chequeo.objects.filter(documento__pk=pk_doc)

    return render(
        request,
        'documento_chequeos.html',
        {
            'pk_proy': pk_proy,
            'documento': doc,
            'listas_chequeo': listas_chequeo,
            'chequeos_doc': chequeos_doc,
            'g_perms': request.user.get_all_permissions(),
        }
    )

@user_passes_test(change_chequeo)
@login_required
def hace_chequeo(request, pk_proy, pk_doc):
    """
    Realiza el control de calidad de un documento a partir de sus chequeos
    """
    doc = get_object_or_404(Documento, pk=pk_doc)
    chequeos_doc = doc.chequeo_documento.all().order_by('tipo_chequeo')
    # chequeos_doc = Chequeo.objects.filter(documento__pk=pk_doc).order_by('tipo_chequeo')

    if request.method == "POST":
        verificados = request.POST.getlist('verificado')
        aplica = request.POST.getlist('aplica')
        for chequeo in chequeos_doc:
            if chequeo.aplica:
                if str(chequeo.pk) in aplica:
                    # Aplicaba y aplica
                    if str(chequeo.pk) in verificados:
                        if not chequeo.verificado:
                            chequeo.verificado = True
                            chequeo.verificado_por = request.user
                    else:
                        if chequeo.verificado:
                            chequeo.verificado = False
                            chequeo.verificado_por = request.user
                else:
                    # Aplicaba pero ahora no aplica
                    chequeo.aplica = False
                    chequeo.verificado = False
                    chequeo.verificado_por = request.user
            else:
                if str(chequeo.pk) in aplica:
                    # No aplicaba pero ahora aplica
                    chequeo.aplica = True
                    chequeo.verificado_por = request.user
                    if str(chequeo.pk) in verificados:
                        chequeo.verificado = True
                    else:
                        chequeo.verificado = False

            chequeo.save()

    return render(
        request,
        'chequeo_documento.html',
        {
            'documento': doc,
            'chequeos_doc': chequeos_doc,
        }
    )


@user_passes_test(delete_chequeo)
@login_required
def elimina_chequeo(request, pk_proy, pk_doc, pk_chk):
    """
    Elimina un chequeo de un documento
    """
    chequeo = get_object_or_404(Chequeo, pk=pk_chk)
    chequeo.delete()

    return redirect('agrega_chequeo', pk_proy=pk_proy, pk_doc=pk_doc)

@login_required
def estado_calidad(request, pk_proy):
    proyecto = get_object_or_404(Proyecto, pk=pk_proy)
    docs = Documento.objects.filter(proyecto_id=pk_proy, documento_reemplazado_por=None)
    estados = []
    for doc in docs:
        pasa = True
        estado = {'no_verificados': []}
        chks_in_doc = Chequeo.objects.filter(documento=doc)
        estado['documento'] = doc
        for chk in chks_in_doc:
            if chk.aplica and not chk.verificado:
                pasa = False
                estado['no_verificados'].append(chk)

        estado['pasa'] = pasa
        estados.append(estado)

    return render(
        request,
        'estado_calidad.html',
        {
            'estados': estados,
            'proyecto': proyecto
        }
    )


# ----------------------------------------------------------------------
# API REST VIEWs -------------------------------------------------------
# ----------------------------------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chequeo_doc_get(request, pk_doc):
    """
    ---
    """
    if request.method == 'GET':
        doc_check = Documento.objects.get(pk=pk_doc)
        print(doc_check)
        serializer = DocumentoChequeoSerializer(doc_check)
        print(serializer.data)
        return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def chequeo_doc_put(request):
    """
    ---
    """
    if request.method == 'PUT':
        serializer = ChequeoRealizadoSerializer(data=request.data, many=True)
        if serializer.is_valid():
            # print("Antes de llamar al save()")
            serializer.save(owner=request.user)
            # print("Después de llamar al save()")
            return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
