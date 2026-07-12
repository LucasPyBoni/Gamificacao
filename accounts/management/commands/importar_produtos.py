import json
import os
from django.core.management.base import BaseCommand
from accounts.models import Reward

class Command(BaseCommand):
  help = "Importa uma lista de produtos a partir de um arquivo JSON"

  def handle(self, *args, **options):
    # Caminho para o arquivo JSON (ajuste se ele estiver em outra pasta)
    caminho_arquivo = "produtos.json"

    if not os.path.exists(caminho_arquivo):
      self.stdout.write(self.style.ERROR(f'Arquivo {caminho_arquivo} não encontrado'))
      return

    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
      rewards = json.load(f)

    contador = 0
    for item in rewards:
      # O get_or_create evita duplicar se você rodar o comando duas vezes
      reward, criado = Reward.objects.get_or_create(
        name=item['name'],
        defaults={
          'category':item['category'],
          'description':item['description'],
          'coin_cost':item['coin_cost'],
          'stock':item['stock']
        }
      )
      if criado:
          contador += 1

    self.stdout.write(self.style.SUCCESS(f'Sucesso! {contador} novo produtos foram importados.'))