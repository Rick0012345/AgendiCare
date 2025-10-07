from django.db import models
from django.core.validators import RegexValidator
from django.urls import reverse

class Paciente(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome Completo")
    cpf = models.CharField(
        max_length=14, 
        unique=True,
        validators=[RegexValidator(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', 'CPF deve estar no formato XXX.XXX.XXX-XX')],
        verbose_name="CPF"
    )
    telefone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\(\d{2}\)\s\d{4,5}-\d{4}$', 'Telefone deve estar no formato (XX) XXXXX-XXXX')],
        verbose_name="Telefone"
    )
    email = models.EmailField(verbose_name="E-mail")
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    endereco = models.TextField(verbose_name="Endereço")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('paciente_detail', kwargs={'pk': self.pk})

class Medico(models.Model):
    ESPECIALIDADES = [
        ('cardiologia', 'Cardiologia'),
        ('dermatologia', 'Dermatologia'),
        ('ginecologia', 'Ginecologia'),
        ('neurologia', 'Neurologia'),
        ('ortopedia', 'Ortopedia'),
        ('pediatria', 'Pediatria'),
        ('psiquiatria', 'Psiquiatria'),
        ('urologia', 'Urologia'),
        ('clinica_geral', 'Clínica Geral'),
        ('oftalmologia', 'Oftalmologia'),
    ]

    nome = models.CharField(max_length=100, verbose_name="Nome Completo")
    crm = models.CharField(max_length=20, unique=True, verbose_name="CRM")
    especialidade = models.CharField(max_length=50, choices=ESPECIALIDADES, verbose_name="Especialidade")
    telefone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\(\d{2}\)\s\d{4,5}-\d{4}$', 'Telefone deve estar no formato (XX) XXXXX-XXXX')],
        verbose_name="Telefone"
    )
    email = models.EmailField(verbose_name="E-mail")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"
        ordering = ['nome']

    def __str__(self):
        return f"Dr(a). {self.nome} - {self.get_especialidade_display()}"

    def get_absolute_url(self):
        return reverse('medico_detail', kwargs={'pk': self.pk})

class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('agendado', 'Agendado'),
        ('confirmado', 'Confirmado'),
        ('em_andamento', 'Em Andamento'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
        ('faltou', 'Paciente Faltou'),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, verbose_name="Paciente")
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, verbose_name="Médico")
    data_hora = models.DateTimeField(verbose_name="Data e Hora")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='agendado', verbose_name="Status")
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"
        ordering = ['data_hora']
        unique_together = ['medico', 'data_hora']  # Evita conflito de horários

    def __str__(self):
        return f"{self.paciente.nome} - Dr(a). {self.medico.nome} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

    def get_absolute_url(self):
        return reverse('agendamento_detail', kwargs={'pk': self.pk})

    @property
    def status_color(self):
        colors = {
            'agendado': 'primary',
            'confirmado': 'info',
            'em_andamento': 'warning',
            'concluido': 'success',
            'cancelado': 'danger',
            'faltou': 'secondary',
        }
        return colors.get(self.status, 'primary')
