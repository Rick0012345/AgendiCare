from django.contrib import admin
from .models import Paciente, Medico, Agendamento

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'telefone', 'email', 'data_nascimento', 'created_at')
    list_filter = ('data_nascimento', 'created_at')
    search_fields = ('nome', 'cpf', 'email', 'telefone')
    ordering = ('nome',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome', 'cpf', 'data_nascimento')
        }),
        ('Contato', {
            'fields': ('telefone', 'email', 'endereco')
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'crm', 'especialidade', 'telefone', 'email', 'created_at')
    list_filter = ('especialidade', 'created_at')
    search_fields = ('nome', 'crm', 'email', 'telefone')
    ordering = ('nome',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Informações Profissionais', {
            'fields': ('nome', 'crm', 'especialidade')
        }),
        ('Contato', {
            'fields': ('telefone', 'email', 'endereco')
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'medico', 'data_hora', 'status', 'created_at')
    list_filter = ('status', 'medico__especialidade', 'data_hora', 'created_at')
    search_fields = ('paciente__nome', 'medico__nome', 'observacoes')
    ordering = ('-data_hora',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'data_hora'
    
    fieldsets = (
        ('Agendamento', {
            'fields': ('paciente', 'medico', 'data_hora', 'status')
        }),
        ('Observações', {
            'fields': ('observacoes',),
            'classes': ('collapse',)
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('paciente', 'medico')
