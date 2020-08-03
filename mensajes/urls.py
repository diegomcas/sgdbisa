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
]
