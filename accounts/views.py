from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.db.models import F
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import date, timedelta
from django.utils import  timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import update_session_auth_hash, authenticate, login
import csv
from .models import Task, TaskCompletion, CoinTransaction, Reward, RewardRedemption, Employee, Department

def login_view(request):
  if request.user.is_authenticated:
    return redirect('dashboard')

  if request.method == 'POST':
    usuario = request.POST.get('username', '').strip().lower()
    senha = request.POST.get('password','')

    # Autentica o usuário
    user = authenticate(request, username=usuario, password=senha)

    if user is not None:
      login(request, user)
      return redirect('dashboard')
    else:
      messages.error(request, "Usuário ou senha incorretos.")
      return redirect("login")

  return render(request, 'accounts/login.html')

def cadastro(request):
  if request.user.is_authenticated:
    return redirect("dashboard")
    
  if request.method=="POST":
    usuario = request.POST.get("username").strip().lower()
    email = request.POST.get("email").strip().lower()
    senha = request.POST.get("password")

    # 1. Verifica se o usuário ou email já existe para não dar erro de duplicidade
    if User.objects.filter(username=usuario).exists():
      messages.error(request, "Este nome de usuário já está cadastrado.")
      return redirect ("cadastro")

    if User.objects.filter(email=email).exists():
      messages.error(request, "Este e-mail já está cadastrado.")
      return redirect ("cadastro")

    #criação se tudo está certo
    novo_usuario = User.objects.create_user(
      username=usuario,
      email=email,
      password=senha
    )

    #criação o perfil do employee vinculado ao user
    Employee.objects.create(
      user=novo_usuario,
      coins=0,
      department=None
    )

    messages.success(request, 'sua conta foi criada com sucesso!')
    return redirect ("login")

  return render(request, "accounts/cadastro.html")



@login_required
def dashboard(request):
  # transações
  transactions = (
  request.user.employee.transactions.all()[:3]
  )
  #tarefas concluidas
  total_tafs_concluidas = request.user.employee.completed_tasks.count()

  # sequencia
  employee = request.user.employee
  completions = employee.completed_tasks.values_list('completed_at', flat=True)
  completed_dates = {timezone.localdate(dt) for dt in completions}
  sequencia = 0
  today = date.today()
  yesterday = today - timedelta(days=1)
  if today in completed_dates:
    check_date = today
  elif yesterday in completed_dates:
    check_date = yesterday
  else:
    check_date = None

  while check_date and check_date in completed_dates:
    sequencia += 1
    check_date -= timedelta(days=1)

  #vai pro dash
  context = {
    "coins": request.user.employee.coins,
    "transactions":transactions,
    "total_tafs_concluidas":total_tafs_concluidas,
    "sequencia":sequencia
    
  }

  

  return render(
    request, 
    'dashboard/dashboard.html', 
    context
    )

# Create your views here.
@login_required
def task_list(request):
  status_atual = request.GET.get("status", "disponiveis")
  employee = request.user.employee

  dificuldade_filtrada = request.GET.get('dificuldade')
  # Criamos um dicionário onde a classe 'active' só vai para o botão da aba atual
  classes_abas = {
    "disponiveis": "active" if status_atual=="disponiveis" else "",
    "em_revisao": "active" if status_atual=="em_revisao" else "",
    "concluidas": "active" if status_atual=="concluidas" else "",
    "rejeitadas": "active" if status_atual=="rejeitadas" else "",

  }

  if status_atual == "em_revisao":
    tasks = Task.objects.filter(
      completions__employee=employee,
      completions__status='pending'
    )
  elif status_atual == 'concluidas':
    tasks = Task.objects.filter(
      completions__employee=employee,
      completions__status='approved'
    )
  elif status_atual == 'rejeitadas':
    tasks = Task.objects.filter(
      completions__employee=employee,
      completions__status='rejected'
    )

  else:
    hoje = timezone.now().date()
    tasks = Task.objects.filter(is_active=True)


    tasks = tasks.exclude(
      completions__employee=employee,
      completions__completed_at__date=hoje,
    ).exclude(
      is_repeatable=False,
      completions__employee=employee,
      completions__status__in=['pending','approved']
    )

  if dificuldade_filtrada and dificuldade_filtrada in dict(Task.Difficulty.choices):
    tasks = tasks.filter(difficulty=dificuldade_filtrada).order_by("-coin_reward")

  context = {
    "tasks": tasks,
    "status_atual":status_atual,
    "classes_abas":classes_abas,
    "difficulties": Task.Difficulty.choices,
    "dificuldade_filtrada":dificuldade_filtrada
  }

  return render (
    request,
    "tasks/tasks.html",
    context
  )

@login_required
def complete_task(request, task_id):
  if request.method != "POST":
    return redirect("task_list")

  employee = request.user.employee
  task = get_object_or_404(Task, id=task_id)

  #tarefas não repetir
  hoje = timezone.now().date()

  ja_concluiu_hoje = TaskCompletion.objects.filter(
    employee=employee,
    task=task,
    completed_at__date = hoje
  ).exists()

  if ja_concluiu_hoje:
    messages.warning(request, "Você já realizou esta tarefa hoje. Tente novamente amanhã!")
    return redirect("task_list")
  # impede de concluir novamente tarefas únicas
  if (
    not task.is_repeatable and TaskCompletion.objects.filter(
      employee=employee,
      task=task,
    ).exists()
  ):
    messages.warning(request, "Tarefa única. Você já realizou esta tarefa.")
    return redirect("task_list")

  status_inicial = TaskCompletion.Status.APPROVED

  # 2. Define o status com base na dificuldade da tarefa
  if task.difficulty == Task.Difficulty.HARD:
    status_inicial = TaskCompletion.Status.PENDING

  TaskCompletion.objects.create(employee=employee, task=task, status=status_inicial)

  if task.difficulty != Task.Difficulty.HARD:
    CoinTransaction.objects.create(
      employee=employee,
      amount=task.coin_reward,
      transaction_type=CoinTransaction.TransactionType.CREDIT,
      reason=f"Conclusão da tarefa: {task.title}",
    )

    #atualiza o db e envia a mensagem pro usuário
    employee.coins = F("coins") + task.coin_reward
    employee.save(update_fields=["coins"])
    employee.refresh_from_db()

    messages.success(request, f"🎉 Tarefa concluída! Você ganhou {task.coin_reward} moedas.")
  else:
    messages.info(request, "📥 Tarefa enviada com sucesso! Ela passará por revisão antes da liberação das moedas.")
  return redirect("task_list")


@login_required
def store(request):
  # Pega a categoria selecionada na URL (se não tiver, vem None)
  categoria_filtrada = request.GET.get('categoria')
  rewards = Reward.objects.filter(is_active=True).order_by("coin_cost")

  if categoria_filtrada and categoria_filtrada in dict(Reward.Category.choices):
    rewards = rewards.filter(category=categoria_filtrada)

  context = {
      "rewards":rewards,
      "categories":Reward.Category.choices,
      "categoria_filtrada": categoria_filtrada,
  }

  return render(
    request, 
    "store/store.html",
    context
  )

@login_required
def redeem_reward(request, reward_id):
  if request.method != "POST":
    return redirect("store")
  employee = request.user.employee

  reward = get_object_or_404(
    Reward,
    id=reward_id,
    is_active=True,
  )

  if employee.coins < reward.coin_cost:
    messages.warning(
      request, "Você não possui moedas suficientes."
    )
    return redirect("store")

  if reward.stock == 0:
    messages.warning(
      request, 
      "Produto em estoque no momento"
    )
    return redirect("store")

  RewardRedemption.objects.create(
    employee=employee,
    reward=reward,
  )  

  CoinTransaction.objects.create(
    employee=employee,
    amount=reward.coin_cost,
    transaction_type=CoinTransaction.TransactionType.DEBIT,
    reason=f"Resgate: {reward.name}",
  )

  employee.coins = F("coins") - reward.coin_cost
  employee.save(update_fields=["coins"])
  employee.refresh_from_db()

  reward.stock -= 1
  reward.save(update_fields=["stock"])
  reward.refresh_from_db()

  messages.success(
    request,
    f"Você resgatou {reward.name}!"
  )

  return redirect("store")

@login_required
def history_transactions(request):
  # transações
  all_transactions = (
  request.user.employee.transactions.all().order_by('-created_at')
  )
  # is_full_page = request.GET.get('full', 'false') == True

  context = {
    "all_transactions":all_transactions,
    }

  return render(
    request,
    "dashboard/history_transactions.html",
    context
  )

@login_required
def configuration(request):
  if request.method == 'POST' and 'btn_senha' in request.POST:
    senha_atual = request.POST.get('senha_atual')
    nova_senha = request.POST.get('nova_senha')

    # Valida se a senha atual está correta
    if not request.user.check_password(senha_atual):
      messages.error(request, "A senha atual informada está incorreta.")
      return redirect('configuration')

    request.user.set_password(nova_senha)
    request.user.save()

    update_session_auth_hash(request, request.user)

    messages.success(request, "Sua senha foi atualizada com sucesso!")
    return redirect('configuration')  

  # se não for admin
  if not request.user.is_staff:
    return render(request, "configuration/configuration.html")

  #busca funcs
  employees = Employee.objects.all()

   # --- NOVA BUSCA: Tarefas aguardando revisão ---
  pending_tasks = TaskCompletion.objects.filter(
    status=TaskCompletion.Status.PENDING
  ).select_related('employee__user', 'task')

  context = {
    "employees":employees,
    "pending_tasks":pending_tasks,
  }

  return render (
    request,
    "configuration/configuration_admin.html",
    context
  )

@login_required
def rejected_task(request, completion_id):
  if request.method == "POST":
    # Busca a conclusão que esteja pendente
    completion = get_object_or_404(
      TaskCompletion, 
      id=completion_id,
      status=TaskCompletion.Status.PENDING
    )

    completion.status = TaskCompletion.Status.REJECTED
    completion.save()
    messages.error(
      request,
      f"A tarefa de {completion.employee.user.username} foi recusada."  
      )
  return redirect('configuration') 

@login_required
def approved_task(request, completion_id):
  if request.method == "POST":
    # Busca a conclusão que esteja aprovada
    completion = get_object_or_404(
      TaskCompletion, 
      id=completion_id,
      status=TaskCompletion.Status.PENDING
    )
    
    employee = completion.employee
    task = completion.task

    # 2. Altera o status para aprovado
    completion.status = TaskCompletion.Status.APPROVED
    completion.save()

    # 3. ADIÇÃO: Gera a transação de moedas no histórico
    CoinTransaction.objects.create(
      employee=employee,
      amount=task.coin_reward,
      transaction_type=CoinTransaction.TransactionType.CREDIT,
      reason=f"Aprovação da tarefa: {task.title}",
    )
    # Atualiza o saldo do funcionário com segurança (usando F)
    employee.coins = F("coins") + task.coin_reward
    employee.save(update_fields=["coins"])

    messages.success(
      request,
      f"A tarefa de {employee.user.username} foi aprovada."  
      )
  return redirect('configuration') 

@login_required
def ranking(request):
    return render (
    request,
    "ranking/ranking.html",
  )

@login_required
def reports(request):
  tipo_filtro = request.GET.get('tipo', 'geral')
  # premio resgatados por employee
  rewards_query = RewardRedemption.objects.all()
  coins_query = CoinTransaction.objects.filter(transaction_type='credit')
  tasks_approved_query = TaskCompletion.objects.filter(status='approved')

  if tipo_filtro == 'usuario':
    rewards_query = RewardRedemption.objects.filter(employee=request.user.employee)
    coins_query = CoinTransaction.objects.filter(employee=request.user.employee)
    tasks_approved_query = TaskCompletion.objects.filter(employee=request.user.employee)

  total_recompensas = rewards_query.count()

  # Total de Recompensas Resgatadas
  rewards_resgatados = RewardRedemption.objects.filter(employee=request.user.employee)

  #moedas emitidas
  resultado_soma = coins_query.aggregate(total=Sum('amount'))
  total_moedas_emitidas =  resultado_soma['total'] or 0

  # taxa de engajamento por employee
  total_tarefas_ativas = Task.objects.filter(is_active=True).count()
  total_tarefas_aprovadas = tasks_approved_query.count()

  # Evita divisão por zero se o sistema não tiver tarefas cadastradas ainda
  if total_tarefas_ativas > 0:
    taxa_engajamento = int((float(total_tarefas_aprovadas)/float(total_tarefas_ativas)) * 100)
  else: 
    taxa_engajamento = 0


  context = {
    "total_recompensas":total_recompensas,
    "total_moedas_emitidas":total_moedas_emitidas,
    "taxa_engajamento":taxa_engajamento,
    "tipo_filtro":tipo_filtro
  }

  return render (
    request,
    "reports/reports.html",
    context
  )

@login_required
def api_moedas_departamento(request):
  dados = TaskCompletion.objects.filter(
    status="APPROVED"
  ).values(
    'employee__department'
  ).annotate(
    total=Sum('task__coin_reward')
  )

  resultado = {item['employee__department']: item['total'] for item in dados}

  return JsonResponse(resultado)

@login_required
def perfil(request):
  employee = request.user.employee
  recompensas = RewardRedemption.objects.filter(
    employee=request.user.employee
  ).select_related('reward')

  if request.method == 'POST':

    #sobre department
    id_departamento = request.POST.get('departamento')
    if id_departamento:
      dept = get_object_or_404(Department, id=id_departamento)
      employee.department = dept
    else:
      employee.department = None

    #sobre perfil
    novo_nome = request.POST.get('nome_completo')
    if novo_nome:
      request.user.first_name = novo_nome

    novo_email = request.POST.get('novo_email')
    if novo_email and novo_email.strip().lower():
      request.user.email = novo_email.strip().lower()

    request.user.save()

    nova_foto = request.FILES.get('avatar')
    if nova_foto:
      employee.avatar = nova_foto

    employee.save()
    messages.success(request, "Perfil atualizado com sucesso!")
    return redirect('perfil')

  context = {
    'employee':employee,
    'recompensas':recompensas,
    'departamentos':Department.objects.all().order_by('department_name')
  }

  return render (
    request,
    "accounts/perfil.html",
    context
  )

@login_required
def exportar_conclusoes_csv(request):
      # 1. Cria a resposta indicando que é um arquivo CSV para download
  response = HttpResponse(content_type='text/csv; charset=utf-8')
  response['Content-Disposition'] = 'attachment; filename="relatorios_tarefas.csv'
  # Para o Excel ler os acentos em português corretamente (BOM)
  response.write(u'\ufeff'.encode('utf8'))

  writer = csv.writer(response, delimiter=';')
  # 2. Escreve a linha de cabeçalho (as colunas do seu Excel)
  writer.writerow(['Colaborador', 'Tarefa', 'Moedas', 'Status', 'Data de Conclusão'])

  tipo_filtro = request.GET.get('tipo', 'geral')

  # 3. Busca os dados puros no banco de dados
  conclusoes = TaskCompletion.objects.all().select_related('employee__user', 'task')

  if tipo_filtro == 'usuario':
    conclusoes = conclusoes.filter(employee=request.user.employee)

  # 4. Escreve os dados linha por linha
  for c in conclusoes:
    writer.writerow([
      c.employee.user.username,
      c.task.title,
      c.task.coin_reward,
      c.get_status_display(),
      c.completed_at.strftime('%d/%m/%Y %H:%M')
    ])

  return response
  


