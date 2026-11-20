from django.db import models
import uuid

# Create your models here.

class Cliente(models.Model):
    class TipoCliente(models.TextChoices):
        COMUM = 'COMUM', 'Comum'
        VIP = 'VIP', 'VIP'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100) #tirei o default
    cpf = models.CharField(max_length=11, default='')
    email = models.EmailField(max_length=100)
    telefone = models.CharField(max_length=20, default='')
    tipo = models.CharField(
        max_length=10,
        choices=TipoCliente.choices,
        default=TipoCliente.COMUM,
    )