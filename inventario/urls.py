from django.contrib import admin
from django.urls import path
from inventario import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.listar, name='listar'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('crear/', views.crear, name='crear'),
    path('eliminar/<int:id>/', views.eliminar, name='eliminar'),
    path('editar/<int:id>/', views.editar, name='editar'),  # <-- Nueva ruta de edición
]