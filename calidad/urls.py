from django.urls import path
from calidad import views

urlpatterns = [
    path(
        'listas_chequeo/',
        views.listas_chequeo,
        name='listas_chequeo'
    ),
    path(
        'lista_chequeo/<int:pk_lc>/view/',
        views.ver_lista_chequeo,
        name='ver_lista_chequeo'
    ),
    path(
        'lista_chequeo/create/',
        views.nueva_lista_chequeo,
        name='nueva_lista_chequeo'
    ),
    path(
        'lista_chequeo/<int:pk_lc>/update/',
        views.edita_lista_chequeo,
        name='edita_lista_chequeo'
    ),
    path(
        'lista_chequeo/<int:pk_lc>/delete/',
        views.elimina_lista_chequeo,
        name='elimina_lista_chequeo'
    ),
    path(
        'tipos_chequeo/',
        views.tipos_chequeo,
        name='tipos_chequeo'
    ),
    path(
        'tipo_chequeo/<int:pk_tc>/view/',
        views.ver_tipo_chequeo,
        name='ver_tipo_chequeo'
    ),
    path(
        'tipo_chequeo/create/',
        views.nuevo_tipo_chequeo,
        name='nuevo_tipo_chequeo'
    ),
    path(
        'tipo_chequeo/<int:pk_tc>/update/',
        views.edita_tipo_chequeo,
        name='edita_tipo_chequeo'
    ),
    path(
        'tipo_chequeo/<int:pk_tc>/delete/',
        views.elimina_tipo_chequeo,
        name='elimina_tipo_chequeo'
    ),
    path(
        'proyecto/<int:pk_proy>/documento/<int:pk_doc>/add_chequeo/',
        views.agrega_chequeo,
        name='agrega_chequeo'
    ),
    path(
        'proyecto/<int:pk_proy>/documento/<int:pk_doc>/make_chequeo/',
        views.hace_chequeo,
        name='hace_chequeo'
    ),
    path(
        'proyecto/<int:pk_proy>/documento/<int:pk_doc>/chequeo/<int:pk_chk>/delete/',
        views.elimina_chequeo,
        name='elimina_chequeo'
    ),
    path(
        'proyecto/<int:pk_proy>/calidad/',
        views.estado_calidad,
        name='estado_calidad'
    ),
    # ----------------------------------------------------------------------
    # API REST URLs --------------------------------------------------------
    # ----------------------------------------------------------------------
    # Lista Los Chequeos del documento "pk_doc"
    path('api-doc-chequeo/<int:pk_doc>/get/', views.chequeo_doc_get),
    # Recibe checks y actualiza estado en la Base de Datos
    path('api-doc-chequeo/put/', views.chequeo_doc_put),
]
