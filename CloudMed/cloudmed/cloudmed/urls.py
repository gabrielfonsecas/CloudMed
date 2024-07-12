from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView
from django.conf.urls import handler404, handler500
from core import views
from core.views import menu, cadastro, nova_consulta, consultas, pacientes, apagar_paciente, editar_paciente


urlpatterns = [
    path('', views.IndexView.as_view(template_name='core/index.html'), name='index.html'),
    path('verificar_cpf/', views.verificar_cpf, name='verificar_cpf'),
    path('verificar_cpf_responsavel/', views.verificar_cpf_responsavel, name='verificar_cpf_responsavel'),
    path('menu/', login_required(menu), name='menu.html'),
    path('cadastro/', cadastro, name='cadastro'),
    path('nova_consulta/', nova_consulta, name='nova_consulta'),
    path('consultas/', consultas, name='consultas'),
    path('pacientes/', pacientes, name='pacientes'),
    path('apagar_paciente/<int:id_paciente>/',
         apagar_paciente, name='apagar_paciente'),
    path('editar_paciente/<int:id_paciente>/',
         editar_paciente, name='editar_paciente'),   
    path('logout/', auth_views.LogoutView.as_view(template_name='core/logout.html'), name='logout'),
]


handler404 = 'core.views.custom_404'

handler500 = 'core.views.custom_500'