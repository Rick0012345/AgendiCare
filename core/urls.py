from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # URLs para Pacientes
    path('pacientes/', views.PacienteListView.as_view(), name='paciente_list'),
    path('pacientes/novo/', views.PacienteCreateView.as_view(), name='paciente_create'),
    path('pacientes/<int:pk>/', views.PacienteDetailView.as_view(), name='paciente_detail'),
    path('pacientes/<int:pk>/editar/', views.PacienteUpdateView.as_view(), name='paciente_update'),
    path('pacientes/<int:pk>/excluir/', views.PacienteDeleteView.as_view(), name='paciente_delete'),
    
    # URLs para Médicos
    path('medicos/', views.MedicoListView.as_view(), name='medico_list'),
    path('medicos/novo/', views.MedicoCreateView.as_view(), name='medico_create'),
    path('medicos/<int:pk>/', views.MedicoDetailView.as_view(), name='medico_detail'),
    path('medicos/<int:pk>/editar/', views.MedicoUpdateView.as_view(), name='medico_update'),
    path('medicos/<int:pk>/excluir/', views.MedicoDeleteView.as_view(), name='medico_delete'),
    
    # URLs para Agendamentos
    path('agendamentos/', views.AgendamentoListView.as_view(), name='agendamento_list'),
    path('agendamentos/novo/', views.AgendamentoCreateView.as_view(), name='agendamento_create'),
    path('agendamentos/<int:pk>/', views.AgendamentoDetailView.as_view(), name='agendamento_detail'),
    path('agendamentos/<int:pk>/editar/', views.AgendamentoUpdateView.as_view(), name='agendamento_update'),
    path('agendamentos/<int:pk>/excluir/', views.AgendamentoDeleteView.as_view(), name='agendamento_delete'),
    
    # URL para atualizar status do agendamento
    path('agendamentos/<int:pk>/status/', views.atualizar_status_agendamento, name='atualizar_status_agendamento'),
]