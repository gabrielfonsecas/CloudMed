from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cadastro, Nova_Consulta
from datetime import date
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from django.http import JsonResponse

def verificar_cpf(request):
    cpf = request.GET.get('cpf', '')
    cpf_existe = Cadastro.objects.filter(cpf=cpf).exists()
    return JsonResponse({'cpf_existe': cpf_existe})

def verificar_cpf_responsavel(request):
    cpf_responsavel = request.GET.get('cpf_responsavel', '')
    cpf_responsavel_existe = Cadastro.objects.filter(cpf=cpf_responsavel).exists()  
    return JsonResponse({'cpf_responsavel_existe': cpf_responsavel_existe})

class IndexView(LoginView):
    template_name = 'index.html'

class CustomLogoutView(auth_views.LogoutView):
    template_name = 'logout.html'

@login_required
def menu(request):
    if request.user.is_authenticated:
        return render(request, 'core/menu.html')
    else:
        return redirect('login')


@login_required
def cadastro(request):
    if request.method == 'POST':
        novo_paciente = Cadastro(
            nome=request.POST.get('nome'),
            sobrenome=request.POST.get('sobrenome'),
            data_nascimento=request.POST.get('data_nascimento'),
            sexo=request.POST.get('sexo'),
            tipo_sanguineo=request.POST.get('tipo_sanguineo'),
            telefone=request.POST.get('telefone'),
            cpf=request.POST.get('cpf'),
            rg=request.POST.get('rg'),
            endereco=request.POST.get('endereco'),
            responsavel=request.POST.get('responsavel'),
            cpf_responsavel=request.POST.get('cpf_responsavel'),
            rg_responsavel=request.POST.get('rg_responsavel'),
        )
        novo_paciente.save()
        return redirect('pacientes')  # Redireciona para a view 'pacientes'
    return render(request, 'core/cadastro.html')


@login_required
def pacientes(request):
    pacientes = Cadastro.objects.all()
    paciente = None

    if request.method == 'POST':
        paciente_id = request.POST.get('id_paciente')
        if paciente_id:
            paciente = get_object_or_404(Cadastro, id_paciente=paciente_id)
        else:
            # Redireciona para a mesma página se o id_paciente estiver vazio
            return redirect('pacientes')

    return render(request, 'core/pacientes.html', {'pacientes': pacientes, 'paciente': paciente})


@login_required
def nova_consulta(request):
    if request.method == 'POST':
        paciente_id = request.POST.get('paciente_consulta')
        data_consulta = request.POST.get('data_consulta')
        anamnese = request.POST.get('anamnese')
        peso = request.POST.get('peso')
        altura = request.POST.get('altura')
        observacao = request.POST.get('observacao')

        if paciente_id:
            paciente = get_object_or_404(Cadastro, id_paciente=paciente_id)
            nova_consulta = Nova_Consulta(
                paciente=paciente,
                data_consulta=data_consulta,
                anamnese=anamnese,
                peso=peso,
                altura=altura,
                observacao=observacao
            )
            nova_consulta.save()
            return redirect('consultas')

    pacientes = Cadastro.objects.all()
    return render(request, 'core/nova_consulta.html', {'pacientes': pacientes})


@login_required
def consultas(request):
    consultas = Nova_Consulta.objects.select_related(
        'paciente').all()  # Otimiza a consulta

    for consulta in consultas:
        # Calcular idade do paciente
        hoje = date.today()
        consulta.paciente.idade = hoje.year - consulta.paciente.data_nascimento.year - \
            ((hoje.month, hoje.day) < (consulta.paciente.data_nascimento.month,
             consulta.paciente.data_nascimento.day))

    return render(request, 'core/consultas.html', {'consultas': consultas})


@login_required
def apagar_paciente(request, id_paciente):
    paciente = get_object_or_404(Cadastro, id_paciente=id_paciente)
    paciente.delete()
    return redirect('pacientes')


@login_required
def editar_paciente(request, id_paciente):
    paciente = get_object_or_404(Cadastro, id_paciente=id_paciente)

    if request.method == 'POST':
        # 1. Obter os dados do formulário
        paciente.nome = request.POST.get('nome')
        paciente.sobrenome = request.POST.get('sobrenome')
        paciente.data_nascimento = request.POST.get('data_nascimento')
        paciente.sexo = request.POST.get('sexo')
        paciente.tipo_sanguineo = request.POST.get('tipo_sanguineo')
        paciente.telefone = request.POST.get('telefone')
        paciente.cpf = request.POST.get('cpf')
        paciente.rg = request.POST.get('rg')
        paciente.endereco = request.POST.get('endereco')
        paciente.responsavel = request.POST.get('responsavel')
        paciente.cpf_responsavel = request.POST.get('cpf_responsavel')
        paciente.rg_responsavel = request.POST.get('rg_responsavel')

        # 3. Salvar as alterações no banco de dados
        paciente.save()

        # 4. Redirecionar para a página de pacientes
        return redirect('pacientes')

    # Se a requisição não for POST, exibir o formulário de edição
    return render(request, 'core/editar_paciente.html', {'paciente': paciente})

def custom_404(request, exception):
    return render(request, 'core/404.html', status=404)

def custom_500(request):
    return render(request, 'core/500.html', status=500)