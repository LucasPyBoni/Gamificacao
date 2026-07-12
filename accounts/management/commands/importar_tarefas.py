import json
import os
from django.core.management.base import BaseCommand
from accounts.models import Task

class Command(BaseCommand):
    help = "Importa uma lista de tarefas a partir de um arquivo JSON"

    def handle(self, *args, **options):
        caminho_arquivo = 'tarefas.json' 

        if not os.path.exists(caminho_arquivo):
            self.stdout.write(self.style.ERROR(f'Arquivo {caminho_arquivo} não encontrado.'))
            return

        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            tarefas = json.load(f)

        contador = 0
        for item in tarefas:
            # get_or_create baseado no título para não duplicar nem mexer nas 8 que você já tem
            task, criado = Task.objects.get_or_create(
                title=item['title'],
                defaults={
                    'description': item['description'],
                    'difficulty': item['difficulty'],
                    'coin_reward': item['coin_reward'],
                    'is_active': True,
                    'is_repeatable': False
                }
            )
            if criado:
                contador += 1

        self.stdout.write(self.style.SUCCESS(f'Sucesso! {contador} novas tarefas foram importadas.'))
