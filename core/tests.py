"""Testes do app core. Rode com: python manage.py test"""

import shutil
import tempfile
from io import StringIO

from django.contrib.admin.sites import site
from django.core.management import CommandError, call_command
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from projetos.models import Print, Projeto
from tecnologias.models import Tecnologia

from .models import Perfil
from .views import linhas_do_terminal

# Os testes que salvam imagens usam uma pasta temporária, pra não sujar a media/ de verdade
MEDIA_TEMPORARIA = tempfile.mkdtemp()


def tearDownModule():
    shutil.rmtree(MEDIA_TEMPORARIA, ignore_errors=True)


class PerfilTests(TestCase):
    def setUp(self):
        self.perfil = Perfil(
            nome="Thiago Limeira de Oliveira",
            sobre="Primeiro parágrafo.\n\nSegundo parágrafo.\n\n",
            destaques="ADS · Estácio\n\nPython · Django",
            github_url="https://github.com/thigo1000/",
        )

    def test_iniciais_e_nomes(self):
        self.assertEqual(self.perfil.iniciais, "TL")
        self.assertEqual(self.perfil.primeiro_nome, "Thiago")
        self.assertEqual(self.perfil.nome_curto, "Thiago Limeira")

    def test_paragrafos_ignoram_linhas_vazias_sobrando(self):
        self.assertEqual(self.perfil.paragrafos_sobre, ["Primeiro parágrafo.", "Segundo parágrafo."])

    def test_destaques_viram_pares(self):
        self.assertEqual(self.perfil.lista_destaques, [("ADS", "Estácio"), ("Python", "Django")])

    def test_usuario_do_github_sai_da_url(self):
        self.assertEqual(self.perfil.usuario_github, "thigo1000")

    def test_admin_nao_deixa_criar_segundo_perfil(self):
        admin_perfil = site._registry[Perfil]
        request = RequestFactory().get("/")
        self.assertTrue(admin_perfil.has_add_permission(request))
        self.perfil.email = "a@b.com"
        self.perfil.save()
        self.assertFalse(admin_perfil.has_add_permission(request))


class HomeTests(TestCase):
    def test_home_funciona_com_banco_vazio(self):
        # Antes de carregar o conteúdo, o site não pode quebrar
        resposta = self.client.get(reverse("core:home"))
        self.assertEqual(resposta.status_code, 200)

    def test_linhas_do_terminal(self):
        projetos = [
            Projeto(slug="cpcc", status=Projeto.Status.NO_AR),
            Projeto(slug="ia", status=Projeto.Status.PLANEJAMENTO),
            Projeto(slug="blog", status=Projeto.Status.PLANEJAMENTO),
        ]
        linhas = linhas_do_terminal(projetos)
        self.assertEqual(linhas[0], {"cor": "g", "texto": "no ar ........... cpcc"})
        self.assertEqual(linhas[1], {"cor": "d", "texto": "planejamento .... ia, blog"})
        self.assertEqual(len(linhas), 2)  # status sem projeto não gera linha


@override_settings(MEDIA_ROOT=MEDIA_TEMPORARIA)
class CarregarConteudoTests(TestCase):
    def test_carrega_tudo_e_a_home_mostra(self):
        call_command("carregar_conteudo", stdout=StringIO())  # StringIO engole a mensagem de "Pronto"
        self.assertEqual(Perfil.objects.count(), 1)
        self.assertEqual(Projeto.objects.count(), 6)
        self.assertEqual(Print.objects.count(), 4)
        self.assertEqual(Tecnologia.objects.count(), 15)

        resposta = self.client.get(reverse("core:home"))
        self.assertContains(resposta, "Thiago Limeira de Oliveira")
        self.assertContains(resposta, "Agendamento de massagem")
        self.assertContains(resposta, "gestao-condominio/README.md")
        self.assertContains(resposta, "no ar ........... cpcc-agendamento")

    def test_nao_roda_duas_vezes(self):
        call_command("carregar_conteudo", stdout=StringIO())
        with self.assertRaises(CommandError):
            call_command("carregar_conteudo", stdout=StringIO())
        self.assertEqual(Projeto.objects.count(), 6)  # nada duplicado
