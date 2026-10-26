"""Testes do app tecnologias. Rode com: python manage.py test"""

from django.test import TestCase
from django.urls import reverse

from .models import Tecnologia


class ColunasTests(TestCase):
    def test_cada_tecnologia_vai_pra_sua_coluna(self):
        Tecnologia.objects.create(nome="Python", status=Tecnologia.Status.APRENDI)
        Tecnologia.objects.create(nome="PostgreSQL", status=Tecnologia.Status.APRENDENDO)
        Tecnologia.objects.create(nome="Power BI", status=Tecnologia.Status.QUERO)

        colunas = self.client.get(reverse("core:home")).context["colunas_tecnologia"]

        nomes = {c["titulo"]: [t.nome for t in c["itens"]] for c in colunas}
        self.assertEqual(nomes, {
            "Já aprendi": ["Python"],
            "Estou aprendendo": ["PostgreSQL"],
            "Quero aprender": ["Power BI"],
        })

    def test_ordem_manda_na_lista(self):
        Tecnologia.objects.create(nome="Zeta", status=Tecnologia.Status.QUERO, ordem=1)
        Tecnologia.objects.create(nome="Alfa", status=Tecnologia.Status.QUERO, ordem=2)
        self.assertEqual([t.nome for t in Tecnologia.objects.all()], ["Zeta", "Alfa"])
