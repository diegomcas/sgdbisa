from django.urls import path
from documental import views

urlpatterns = [
    path(
        'proyectos',
        views.proyectos,
        name='proyectos'
    ),
    path(
        'proyecto/<int:primary_key>/finalize/',
        views.finalizar_proyecto,
        name='finalizar_proyecto'
    ),
    path(
        'proyecto/<int:primary_key>/view/',
        views.ver_proyecto,
        name='ver_proyecto'
    ),
    path(
        'proyecto/create/',
        views.nuevo_proyecto,
        name='nuevo_proyecto'
    ),
    path(
        'proyecto/<int:primary_key>/update/',
        views.edita_proyecto,
        name='edita_proyecto'
    ),
    path(
        'proyecto/<int:pk_proy>/documento/<int:pk_doc>/view/',
        views.ver_documento,
        name='ver_documento'
    ),
    path(
        'proyecto/<int:pk_proy>/documento/create/',
        views.nuevo_documento,
        name='nuevo_documento'
    ),
    path(
        'proyecto/<int:pk_proy>/documento/<int:pk_doc>/<int:pk_tique>/update/',
        views.edita_documento,
        name='edita_documento'
    ),
    path(
        'proyecto/<int:pk_proy>/documento/<int:pk_doc>/<int:pk_tique>/obs/',
        views.observacion_documento,
        name='observacion_documento'
    ),
    path(
        'proyecto/<int:pk_proy>/documento/<int:pk_doc>/<int:pk_tique>/revision/',
        views.revision_documento,
        name='revision_documento'
    ),
    path(
        'proyecto/<int:pk_proy>/documento/<int:pk_doc>/delete/',
        views.elimina_documento,
        name='elimina_documento'
    ),
    path(
        'proyecto/<int:pk_proy>/archivos/',
        views.archivos,
        name='archivos'
    ),
    path(
        'proyecto/<int:pk_proy>/archivo/<int:pk_file>/view/',
        views.ver_archivo,
        name='ver_archivo'
    ),
    path(
        'proyecto/<int:pk_proy>/archivo/create/',
        views.nuevo_archivo,
        name='nuevo_archivo'
    ),
    path(
        'proyecto/<int:pk_proy>/archivo/<int:pk_file>/<int:pk_tique>/update/',
        views.edita_archivo,
        name='edita_archivo'
    ),
    path(
        'proyecto/<int:pk_proy>/archivo/<int:pk_file>/<int:pk_tique>/revision/',
        views.revision_archivo,
        name='revision_archivo'
    ),
    path(
        'proyecto/<int:pk_proy>/archivo/<int:pk_file>/delete/',
        views.elimina_archivo,
        name='elimina_archivo'
    ),
    # ----------------------------------------------------------------------
    # API REST URLs --------------------------------------------------------
    # ----------------------------------------------------------------------
    # Filtra documentos por Nombre o parte del Nombre
    path('api-find-docs/<str:num_doc>', views.find_docs),
]
