from django.db import models


class Tecnologia(models.Model):
    class Status(models.TextChoices):
        APRENDI = "aprendi", "Já aprendi"
        APRENDENDO = "aprendendo", "Estou aprendendo"
        QUERO = "quero", "Quero aprender"

    nome = models.CharField(max_length=60)
    descricao = models.CharField("descrição", max_length=160, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices)
    ordem = models.PositiveIntegerField(default=0, help_text="Menor aparece primeiro")

    class Meta:
        ordering = ["ordem", "nome"]
        verbose_name = "tecnologia"
        verbose_name_plural = "tecnologias"

    def __str__(self):
        return f"{self.nome} ({self.get_status_display()})"
