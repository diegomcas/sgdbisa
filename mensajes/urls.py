from django.urls import path
from mensajes import views


urlpatterns = [
    path(
        'proyecto/<int:pk_proy>/archivo/<int:pk_file>/add_tique/',
        views.agrega_tique_arch,
        name='agrega_tique_arch'
    ),
    path(
        'proyecto/<int:pk_proy>/documento/<int:pk_doc>/add_tique/',
        views.agrega_tique_doc,
        name='agrega_tique_doc'
    ),
    path(
        'tique/<int:pk_tique>/get_tique/',
        views.tomar_tique,
        name='tomar_tique'
    ),
    path(
        'mensaje/<int:pk_msg>/read/',
        views.marcar_leido,
        name='marcar_leido'
    ),
    path(
        'proyecto/<int:pk_proy>/management/',
        views.gestion_tiquet,
        name='gestion_tiquet'
    ),
    path(
        'proyecto/<int:pk_proy>/tique/<int:pk_tique>/delete/',
        views.elimina_tique,
        name='elimina_tique'
    ),
    path(
        'proyecto/<int:pk_proy>/tique/<int:pk_tique>/free/',
        views.libera_tique,
        name='libera_tique'
    ),
]
