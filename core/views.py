from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Paciente, Medico, Agendamento

# Views para Dashboard
def dashboard(request):
    hoje = timezone.now().date()
    agendamentos_hoje = Agendamento.objects.filter(data_hora__date=hoje).order_by('data_hora')
    total_pacientes = Paciente.objects.count()
    total_medicos = Medico.objects.count()
    total_agendamentos = Agendamento.objects.count()
    
    context = {
        'agendamentos_hoje': agendamentos_hoje,
        'total_pacientes': total_pacientes,
        'total_medicos': total_medicos,
        'total_agendamentos': total_agendamentos,
    }
    return render(request, 'core/dashboard.html', context)

# Views para Pacientes
class PacienteListView(ListView):
    model = Paciente
    template_name = 'core/paciente_list.html'
    context_object_name = 'pacientes'
    paginate_by = 10

    def get_queryset(self):
        queryset = Paciente.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nome__icontains=search) | 
                Q(cpf__icontains=search) |
                Q(email__icontains=search)
            )
        return queryset

class PacienteDetailView(DetailView):
    model = Paciente
    template_name = 'core/paciente_detail.html'
    context_object_name = 'paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['agendamentos'] = Agendamento.objects.filter(paciente=self.object).order_by('-data_hora')[:5]
        return context

class PacienteCreateView(CreateView):
    model = Paciente
    template_name = 'core/paciente_form.html'
    fields = ['nome', 'cpf', 'telefone', 'email', 'data_nascimento', 'endereco']
    success_url = reverse_lazy('paciente_list')

    def form_valid(self, form):
        messages.success(self.request, 'Paciente cadastrado com sucesso!')
        return super().form_valid(form)

class PacienteUpdateView(UpdateView):
    model = Paciente
    template_name = 'core/paciente_form.html'
    fields = ['nome', 'cpf', 'telefone', 'email', 'data_nascimento', 'endereco']
    success_url = reverse_lazy('paciente_list')

    def form_valid(self, form):
        messages.success(self.request, 'Paciente atualizado com sucesso!')
        return super().form_valid(form)

class PacienteDeleteView(DeleteView):
    model = Paciente
    template_name = 'core/paciente_confirm_delete.html'
    success_url = reverse_lazy('paciente_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Paciente excluído com sucesso!')
        return super().delete(request, *args, **kwargs)

# Views para Médicos
class MedicoListView(ListView):
    model = Medico
    template_name = 'core/medico_list.html'
    context_object_name = 'medicos'
    paginate_by = 10

    def get_queryset(self):
        queryset = Medico.objects.all()
        search = self.request.GET.get('search')
        especialidade = self.request.GET.get('especialidade')
        
        if search:
            queryset = queryset.filter(
                Q(nome__icontains=search) | 
                Q(crm__icontains=search) |
                Q(email__icontains=search)
            )
        
        if especialidade:
            queryset = queryset.filter(especialidade=especialidade)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['especialidades'] = Medico.ESPECIALIDADES
        return context

class MedicoDetailView(DetailView):
    model = Medico
    template_name = 'core/medico_detail.html'
    context_object_name = 'medico'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['agendamentos'] = Agendamento.objects.filter(medico=self.object).order_by('-data_hora')[:5]
        return context

class MedicoCreateView(CreateView):
    model = Medico
    template_name = 'core/medico_form.html'
    fields = ['nome', 'crm', 'especialidade', 'telefone', 'email']
    success_url = reverse_lazy('medico_list')

    def form_valid(self, form):
        messages.success(self.request, 'Médico cadastrado com sucesso!')
        return super().form_valid(form)

class MedicoUpdateView(UpdateView):
    model = Medico
    template_name = 'core/medico_form.html'
    fields = ['nome', 'crm', 'especialidade', 'telefone', 'email']
    success_url = reverse_lazy('medico_list')

    def form_valid(self, form):
        messages.success(self.request, 'Médico atualizado com sucesso!')
        return super().form_valid(form)

class MedicoDeleteView(DeleteView):
    model = Medico
    template_name = 'core/medico_confirm_delete.html'
    success_url = reverse_lazy('medico_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Médico excluído com sucesso!')
        return super().delete(request, *args, **kwargs)

# Views para Agendamentos
class AgendamentoListView(ListView):
    model = Agendamento
    template_name = 'core/agendamento_list.html'
    context_object_name = 'agendamentos'
    paginate_by = 15

    def get_queryset(self):
        queryset = Agendamento.objects.select_related('paciente', 'medico').all()
        
        # Filtros
        search = self.request.GET.get('search')
        status = self.request.GET.get('status')
        medico = self.request.GET.get('medico')
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')
        
        if search:
            queryset = queryset.filter(
                Q(paciente__nome__icontains=search) | 
                Q(medico__nome__icontains=search)
            )
        
        if status:
            queryset = queryset.filter(status=status)
            
        if medico:
            queryset = queryset.filter(medico_id=medico)
            
        if data_inicio:
            queryset = queryset.filter(data_hora__date__gte=data_inicio)
            
        if data_fim:
            queryset = queryset.filter(data_hora__date__lte=data_fim)
            
        return queryset.order_by('data_hora')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Agendamento.STATUS_CHOICES
        context['medicos'] = Medico.objects.all()
        return context

class AgendamentoDetailView(DetailView):
    model = Agendamento
    template_name = 'core/agendamento_detail.html'
    context_object_name = 'agendamento'

class AgendamentoCreateView(CreateView):
    model = Agendamento
    template_name = 'core/agendamento_form.html'
    fields = ['paciente', 'medico', 'data_hora', 'status', 'observacoes']
    success_url = reverse_lazy('agendamento_list')

    def form_valid(self, form):
        # Verificar se já existe agendamento para o médico no mesmo horário
        data_hora = form.cleaned_data['data_hora']
        medico = form.cleaned_data['medico']
        
        conflito = Agendamento.objects.filter(
            medico=medico, 
            data_hora=data_hora
        ).exclude(pk=self.object.pk if hasattr(self, 'object') else None)
        
        if conflito.exists():
            messages.error(self.request, 'Já existe um agendamento para este médico neste horário!')
            return self.form_invalid(form)
        
        messages.success(self.request, 'Agendamento criado com sucesso!')
        return super().form_valid(form)

class AgendamentoUpdateView(UpdateView):
    model = Agendamento
    template_name = 'core/agendamento_form.html'
    fields = ['paciente', 'medico', 'data_hora', 'status', 'observacoes']
    success_url = reverse_lazy('agendamento_list')

    def form_valid(self, form):
        # Verificar se já existe agendamento para o médico no mesmo horário
        data_hora = form.cleaned_data['data_hora']
        medico = form.cleaned_data['medico']
        
        conflito = Agendamento.objects.filter(
            medico=medico, 
            data_hora=data_hora
        ).exclude(pk=self.object.pk)
        
        if conflito.exists():
            messages.error(self.request, 'Já existe um agendamento para este médico neste horário!')
            return self.form_invalid(form)
        
        messages.success(self.request, 'Agendamento atualizado com sucesso!')
        return super().form_valid(form)

class AgendamentoDeleteView(DeleteView):
    model = Agendamento
    template_name = 'core/agendamento_confirm_delete.html'
    success_url = reverse_lazy('agendamento_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Agendamento excluído com sucesso!')
        return super().delete(request, *args, **kwargs)

# View para atualizar status do agendamento
def atualizar_status_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    
    if request.method == 'POST':
        novo_status = request.POST.get('status')
        if novo_status in dict(Agendamento.STATUS_CHOICES):
            agendamento.status = novo_status
            agendamento.save()
            messages.success(request, f'Status atualizado para {agendamento.get_status_display()}!')
        else:
            messages.error(request, 'Status inválido!')
    
    return redirect('agendamento_detail', pk=pk)
