from django.urls import path
from .views import multimedia_views, ficha_multimedia_list, ficha_multimedia_add, ficha_multimedia_delete

app_name = 'multimedia'

# URLs del CRUD global
urlpatterns = multimedia_views.get_urls()

# URLs para multimedia por ficha
urlpatterns += [
    path('ficha/<int:ficha_pk>/', ficha_multimedia_list, name='ficha_multimedia_list'),
    path('ficha/<int:ficha_pk>/agregar/', ficha_multimedia_add, name='ficha_multimedia_add'),
    path('ficha/<int:ficha_pk>/<int:pk>/eliminar/', ficha_multimedia_delete, name='ficha_multimedia_delete'),
]
