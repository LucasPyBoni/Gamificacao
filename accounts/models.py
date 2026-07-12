from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee")
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    coins = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Department(models.Model):
    department_name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.department_name

class Task(models.Model):
    class Difficulty(models.TextChoices):
        EASY = "easy", "Fácil"
        MEDIUM = "medium", "Média"
        HARD = "hard", "Difícil"

    difficulty = models.CharField(
            max_length=10,
            choices=Difficulty.choices,
            default=Difficulty.EASY,
        )
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    coin_reward=models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    is_repeatable = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return self.title

class TaskCompletion(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Em Revisão"
        APPROVED = "approved", "Aprovada"
        REJECTED = "rejected", "Recusada"

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="completed_tasks",
    )
    
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="completions",
    )
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.APPROVED,
    )

    xp_reward = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-completed_at"]
        verbose_name = "Conclusão de tarefa"
        verbose_name_plural = "Conclusões de tarefas"

    def __str__(self):
        return f"{self.employee} concluiu {self.task}"

class CoinTransaction(models.Model):
    class TransactionType(models.TextChoices):
        CREDIT = "credit", "Crédito",
        DEBIT = "debit", "Débito"

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="transactions",
    )        

    amount = models.PositiveIntegerField()

    transaction_type = models.CharField(
        max_length=10,
        choices=TransactionType.choices,
    )
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Transação"
        verbose_name_plural = "Transações"

    def __str__(self):
        sinal = "+" if self.transaction_type == self.TransactionType.CREDIT else "-"
        return f"{self.employee} {sinal}{self.amount}"

class Reward(models.Model):
    class Category(models.TextChoices):
        FOOD = "food", "Vale-Comida"
        ELETRONICS = "eletronics", "Eletronicos"    
        CLOTHING = "clothing", "Roupa"
        GENERIC = "generic", "Outros"

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    coin_cost = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    category = models.CharField(
        max_length=20, 
        choices=Category.choices,
        default=Category.GENERIC,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Recompensa"
        verbose_name_plural = "Recompensas"

    def __str__(self):
        return self.name


class RewardRedemption(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendente"
        APPROVED = "approved", "Aprovado"
        DELIVERED = "delivered", "Entregue"
        CANCELED = "canceled", "Cancelado"

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="redemptions"
    )

    reward = models.ForeignKey(
        Reward,
        on_delete=models.CASCADE,
        related_name="redemptions"
    )

    redeemed_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.PENDING
    )

    class Meta:
        ordering = ["-redeemed_at"]
        verbose_name = "Resgate"
        verbose_name_plural = "Resgates"

        def __str__(self):
            return f"{self.employee} → {self.reward}"    