from datetime import datetime

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Imovel(models.Model):
    TIPO_CHOICES = [
        ('casa', 'Casa'),
        ('apartamento', 'Apartamento'),
        # Adicione outros tipos de imóveis conforme necessário
    ]

    bairro = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    imobiliaria = models.CharField(max_length=100, default="DeFranco")
    current_date = models.DateField(auto_now_add=True)  # Use auto_now_add para definir a data automaticamente no momento da criação do objeto

    def __str__(self):
        return f"{self.tipo} em {self.bairro} - R$ {self.valor}"

    class Meta:
        verbose_name = "Imóvel"
        verbose_name_plural = "Imóveis"
        ordering = ['bairro', 'valor']


# Signal para definir a data atual antes de salvar o objeto Imovel
@receiver(pre_save, sender=Imovel)
def set_current_date(sender, instance, *args, **kwargs):
    if not instance.pk:  # Verifica se o objeto ainda não foi salvo no banco de dados
        instance.current_date = datetime.now().date()  # Define a data atual apenas quando o objeto está sendo criado