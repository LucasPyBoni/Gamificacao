from django.contrib import admin
from .models import Employee
from .models import Department
from .models import Task
from .models import TaskCompletion
from .models import CoinTransaction
from .models import Reward
from .models import RewardRedemption
# Register your models here.

admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Task)
admin.site.register(TaskCompletion)
admin.site.register(CoinTransaction)
admin.site.register(Reward)
admin.site.register(RewardRedemption)