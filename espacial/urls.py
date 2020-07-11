from django.urls import path
from espacial import views

urlpatterns = [
    path(
        'spacial/<int:pk_object>/<slug:obj>/',
        views.espacial,
        name='espacial'
    ),
    path(
        'mapping/<int:pk_object>/<slug:obj>/',
        views.mapping,
        name='mapping'
    ),
    path(
        'spatial_query/',
        views.consulta_espacial,
        name='consulta_espacial'
    ),
]
