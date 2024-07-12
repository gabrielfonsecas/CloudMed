from django.db import models

class Cadastro(models.Model):
    id_paciente = models.AutoField(primary_key=True)
    nome = models.TextField(null=True, blank=True, max_length=255)
    sobrenome = models.TextField(null=True, blank=True, max_length=255)
    data_nascimento = models.DateField(null=True, blank=True)
    sexo = models.TextField(max_length=10, null=True, blank=True, choices=[
        ('masculino', 'Masculino'),
        ('feminino', 'Feminino'),
        ('outro', 'Outro'),
    ])
    tipo_sanguineo = models.CharField(max_length=10, blank=True, null=True, choices=[
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('o+', 'O+'),
        ('o-', 'O-'),
    ])
    telefone = models.CharField(max_length=20, blank=True, null=True)
    cpf = models.CharField(max_length=14, blank=True, null=True, unique=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)
    responsavel = models.CharField(max_length=255, blank=True, null=True)
    cpf_responsavel = models.CharField(max_length=14, blank=True, null=True, default='')
    rg_responsavel = models.CharField(max_length=20, blank=True, null=True, default='')
    
    def __str__(self):
        return f"{self.nome} {self.sobrenome}"

class Nova_Consulta(models.Model):
    id_consulta = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(Cadastro, on_delete=models.CASCADE)  # Relacionamento com Cadastro
    data_consulta = models.DateField()
    anamnese = models.TextField()
    peso = models.FloatField()
    altura = models.FloatField()
    observacao = models.TextField()
    
    def __str__(self):
        return f"Consulta {self.id_consulta} - Paciente {self.paciente.nome} {self.paciente.sobrenome}"
