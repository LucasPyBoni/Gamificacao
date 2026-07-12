from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),

    path(
      'logout/',
      auth_views.LogoutView.as_view(),
      name='logout'
    ),
    path('cadastro/', views.cadastro, name='cadastro'),

    # Tela para digitar o e-mail de recuperação
    path('reset_password/',
    auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
    name='reset_password'),

    # 2. Tela de aviso que o e-mail foi enviado com sucesso
    path('reset_password_sent/',
    auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
    name='password_reset_done'),

    # Link seguro enviado por e-mail (contém o token de segurança)
    path('reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"),
    name='password_reset_confirm'),

    # Tela de aviso que a senha foi alterada com sucesso
    path('reset_password_complete/',
    auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),
    name='password_reset_complete'),


    path(
      '',
      views.dashboard,
      name='dashboard'
    ),

    path(
      "tasks/", views.task_list, name="task_list"
      ),
      path(
        "<int:task_id>/complete/",
        views.complete_task,
        name="complete_task",
      ),

    path(
      "store/", views.store, name="store"
    ),

    path(
      "store/<int:reward_id>/redeem/",
      views.redeem_reward,
      name="redeem_reward"
    ),

    path(
      "dashboard/", views.history_transactions, name="history_transactions"
    ),

    path(
      'configuration/task/<int:completion_id>/approve/', 
      views.approved_task, 
      name='approved_task',
    ),

    path(
      'configuration/task/<int:completion_id>/reject/', 
      views.rejected_task, 
      name='rejected_task'
    ),

    path(
      "accounts/", views.configuration, name="configuration"
    ),

    path(
      "ranking/", views.ranking, name="ranking"
    ),

    path(
      "perfil/", views.perfil, name="perfil"
    ),

    path(
      "reports/", views.reports, name="reports"
    ),

    path(
      "reports/export-csv", views.exportar_conclusoes_csv, name="exportar_csv"
    ),

    path(
      "reports/api/moedas/", views.api_moedas_departamento, name="api_moedas_departamento"
    ),


]
