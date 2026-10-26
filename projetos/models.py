from urllib.parse import urlparse

from django.db import models
from django.urls import reverse


class ProjetoQuerySet(models.QuerySet):
    """Filtros reutilizáveis: Projeto.objects.construidos() e .planejados()."""

    def construidos(self):
        return self.filter(status__in=Projeto.STATUS_CONSTRUIDOS)

    def planejados(self):
        return self.exclude(status__in=Projeto.STATUS_CONSTRUIDOS)


class Projeto(models.Model):
    class Status(models.TextChoices):
        NO_AR = "no_ar", "no ar"
        EM_DEPLOY = "em_deploy", "em deploy"
        EM_ANDAMENTO = "em_andamento", "em andamento"
        PLANEJAMENTO = "planejamento", "planejamento"

    # Projetos com esses status vão pra seção "O que já construí" (com prints).
    # Os outros vão pra "O que vem por aí" (cartões de especificação).
    STATUS_CONSTRUIDOS = [Status.NO_AR, Status.EM_DEPLOY]

    # Cor do selo de status: ok = verde, warn = laranja, plan = cinza
    CORES_STATUS = {
        Status.NO_AR: "ok",
        Status.EM_DEPLOY: "warn",
        Status.EM_ANDAMENTO: "warn",
        Status.PLANEJAMENTO: "plan",
    }

    # Básico
    nome = models.CharField(max_length=120)
    slug = models.SlugField(
        unique=True,
        help_text="Nome curto usado no endereço e no terminal. Ex.: site-adecin",
    )
    status = models.CharField(max_length=20, choices=Status.choices)
    ordem = models.PositiveIntegerField(default=0, help_text="Menor aparece primeiro")

    # Usados nos projetos construídos
    resumo = models.TextField(blank=True)
    funcionalidades = models.TextField(blank=True, help_text="Uma por linha")
    aprendizado = models.TextField("o que aprendi", blank=True)
    proximo_passo = models.TextField("próximo passo", blank=True)

    # Usados nos projetos em andamento ou planejamento (só aparece o que estiver preenchido)
    problema = models.TextField(blank=True)
    meu_papel = models.TextField("meu papel", blank=True)
    plano = models.TextField(blank=True)
    foco = models.CharField(max_length=200, blank=True)

    # Comum aos dois
    stack = models.CharField(
        max_length=200, blank=True, help_text="Separe por vírgula. Ex.: Python, Django, SQLite"
    )
    url_site = models.URLField("link do site", blank=True)
    url_codigo = models.URLField("link do código", blank=True)
    codigo_privado = models.BooleanField(
        "código privado", default=False, help_text='Mostra "código privado" no lugar do link'
    )

    objects = ProjetoQuerySet.as_manager()

    class Meta:
        ordering = ["ordem", "nome"]

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse("projetos:detalhe", args=[self.slug])

    @property
    def construido(self):
        return self.status in self.STATUS_CONSTRUIDOS

    @property
    def cor_status(self):
        return self.CORES_STATUS.get(self.status, "plan")

    @property
    def dominio(self):
        """"https://cpcc.pythonanywhere.com" -> "cpcc.pythonanywhere.com" (barra do navegador)."""
        return urlparse(self.url_site).netloc if self.url_site else f"{self.slug}.local"

    @property
    def lista_funcionalidades(self):
        return [linha.strip() for linha in self.funcionalidades.splitlines() if linha.strip()]

    @property
    def lista_stack(self):
        return [item.strip() for item in self.stack.split(",") if item.strip()]


class Print(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name="prints")
    imagem = models.ImageField(upload_to="projetos/")
    legenda = models.CharField(
        max_length=40, help_text='Nome da aba embaixo do print. Ex.: "início", "login"'
    )
    texto_alternativo = models.CharField(
        max_length=200, help_text="Descrição da imagem pra leitores de tela e buscadores"
    )
    mostrar_inteira = models.BooleanField(
        default=False,
        help_text="Marque pra prints de celular ou telas estreitas: a imagem aparece inteira, sem cortar",
    )
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["ordem", "id"]

    def __str__(self):
        return f"{self.projeto} · {self.legenda}"
