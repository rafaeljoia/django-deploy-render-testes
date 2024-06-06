from datetime import datetime

from django.db import models

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
    current_date = datetime.date.today()

    def __str__(self):
        return f"{self.tipo} em {self.bairro} - R$ {self.valor}"

    class Meta:
        verbose_name = "Imóvel"
        verbose_name_plural = "Imóveis"
        ordering = ['bairro', 'valor']
