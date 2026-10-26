from django.db import models


class Perfil(models.Model):
    """Dados pessoais que aparecem no topo, no "Sobre mim" e no contato.

    Só existe um perfil. O admin impede criar um segundo (ver core/admin.py).
    """

    nome = models.CharField(max_length=100)
    cargo = models.CharField(
        max_length=100, help_text='Ex.: "Desenvolvedor Python · Django"'
    )
    cidade = models.CharField(max_length=60)

    titulo_sobre = models.CharField(
        "título do Sobre mim",
        max_length=120,
        help_text='Ex.: "De quem atende para quem constrói"',
    )
    sobre = models.TextField(
        "texto do Sobre mim",
        help_text="Separe os parágrafos com uma linha em branco. O primeiro sai maior.",
    )
    destaques = models.TextField(
        blank=True,
        help_text='Um por linha, no formato "Destaque · complemento". Ex.: "ADS · Estácio"',
    )
    foto = models.ImageField(upload_to="perfil/", blank=True)

    email = models.EmailField()
    github_url = models.URLField("GitHub", blank=True)
    linkedin_url = models.URLField("LinkedIn", blank=True)
    texto_contato = models.TextField("texto do contato", blank=True)

    class Meta:
        verbose_name = "perfil"
        verbose_name_plural = "perfil"

    def __str__(self):
        return self.nome

    @property
    def primeiro_nome(self):
        """Usado no logo "~/thiago" do topo."""
        return self.nome.split()[0] if self.nome else ""

    @property
    def nome_curto(self):
        """Dois primeiros nomes, pro "whoami" do terminal. "Thiago Limeira de Oliveira" -> "Thiago Limeira"."""
        return " ".join(self.nome.split()[:2])

    @property
    def iniciais(self):
        """Usado no lugar da foto enquanto ela não for enviada. "Thiago Limeira" -> "TL"."""
        return "".join(p[0] for p in self.nome_curto.split()).upper()

    @property
    def paragrafos_sobre(self):
        """Quebra o texto em parágrafos usando as linhas em branco."""
        return [p.strip() for p in self.sobre.split("\n\n") if p.strip()]

    @property
    def lista_destaques(self):
        """Transforma "ADS · Estácio" em ("ADS", "Estácio") pra deixar a 1ª parte em negrito."""
        itens = []
        for linha in self.destaques.splitlines():
            if not linha.strip():
                continue
            destaque, _, complemento = linha.partition("·")
            itens.append((destaque.strip(), complemento.strip()))
        return itens

    @property
    def usuario_github(self):
        """"https://github.com/thigo1000" -> "thigo1000"."""
        return self.github_url.rstrip("/").rsplit("/", 1)[-1]

    @property
    def usuario_linkedin(self):
        return self.linkedin_url.rstrip("/").rsplit("/", 1)[-1]


class Experiencia(models.Model):
    cargo = models.CharField(max_length=100)
    empresa = models.CharField(
        "empresa e detalhes",
        max_length=200,
        help_text="Aparece embaixo do cargo. Pode juntar várias empresas separadas por ·",
    )
    periodo = models.CharField(
        max_length=40, help_text='Texto livre. Ex.: "09/2025 – atual", "anteriormente"'
    )
    ordem = models.PositiveIntegerField(default=0, help_text="Menor aparece primeiro")

    class Meta:
        ordering = ["ordem"]
        verbose_name = "experiência"
        verbose_name_plural = "experiências"

    def __str__(self):
        return f"{self.cargo} · {self.empresa}"


class Formacao(models.Model):
    curso = models.CharField(max_length=120)
    instituicao = models.CharField(
        "instituição e detalhes", max_length=160, help_text='Ex.: "Estácio · Graduação tecnológica"'
    )
    periodo = models.CharField(max_length=40)
    ordem = models.PositiveIntegerField(default=0, help_text="Menor aparece primeiro")

    class Meta:
        ordering = ["ordem"]
        verbose_name = "formação"
        verbose_name_plural = "formações"

    def __str__(self):
        return self.curso
