from django.db import models
import uuid

# Create your models here.

class TipoProduto(models.TextChoices):
    FISICO = 'FISICO'
    DIGITAL = 'DIGITAL'

class Produto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tipo = models.CharField(max_length=10, choices=TipoProduto.choices, default=TipoProduto.FISICO)
    estoque = models.PositiveIntegerField(blank=True, null=True)
    tamanho_arquivo = models.PositiveIntegerField(blank=True, null=True)
    peso = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
