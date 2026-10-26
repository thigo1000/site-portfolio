"""Testes do app projetos. Rode com: python manage.py test"""

from django.test import TestCase
from django.urls import reverse

from .models import Projeto


class ProjetoModelTests(TestCase):
    def setUp(self):
        self.no_ar = Projeto.objects.create(
            nome="Agendamento", slug="cpcc-agendamento", status=Projeto.Status.NO_AR,
            url_site="https://cpcc.pythonanywhere.com", stack="Python, Django,  , SQLite",
            funcionalidades="Login\n\nAgenda\n",
        )
        self.deploy = Projeto.objects.create(nome="ADECIN", slug="site-adecin", status=Projeto.Status.EM_DEPLOY)
        self.plano = Projeto.objects.create(
            nome="IA da EBD", slug="ia-ebd", status=Projeto.Status.PLANEJAMENTO, problema="Dúvidas entre aulas"
        )

    def test_separacao_construidos_e_planejados(self):
        self.assertQuerySetEqual(Projeto.objects.construidos(), [self.no_ar, self.deploy], ordered=False)
        self.assertQuerySetEqual(Projeto.objects.planejados(), [self.plano])

    def test_dominio_e_listas(self):
        self.assertEqual(self.no_ar.dominio, "cpcc.pythonanywhere.com")
        self.assertEqual(self.no_ar.lista_stack, ["Python", "Django", "SQLite"])  # ignora item vazio
        self.assertEqual(self.no_ar.lista_funcionalidades, ["Login", "Agenda"])

    def test_cor_do_status(self):
        self.assertEqual(self.no_ar.cor_status, "ok")
        self.assertEqual(self.deploy.cor_status, "warn")
        self.assertEqual(self.plano.cor_status, "plan")


class ProjetoViewTests(TestCase):
    def setUp(self):
        self.projeto = Projeto.objects.create(
            nome="IA da EBD", slug="ia-ebd", status=Projeto.Status.PLANEJAMENTO,
            problema="Alunos têm dúvidas entre uma aula e outra",
        )

    def test_pagina_do_projeto(self):
        resposta = self.client.get(reverse("projetos:detalhe", args=["ia-ebd"]))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Alunos têm dúvidas entre uma aula e outra")
        # Campo vazio não aparece na ficha
        self.assertNotContains(resposta, "<dt>meu papel</dt>", html=True)

    def test_projeto_inexistente_da_404(self):
        resposta = self.client.get(reverse("projetos:detalhe", args=["nao-existe"]))
        self.assertEqual(resposta.status_code, 404)

    def test_lista_redireciona_para_a_home(self):
        resposta = self.client.get(reverse("projetos:lista"))
        self.assertRedirects(resposta, reverse("core:home") + "#projetos", fetch_redirect_response=False)
