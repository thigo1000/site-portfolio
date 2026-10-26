from django.shortcuts import render

from projetos.models import Projeto
from tecnologias.models import Tecnologia

from .models import Experiencia, Formacao

# Cor de cada status dentro do terminal (classes do CSS: g = verde, y = amarelo, d = cinza)
COR_NO_TERMINAL = {"ok": "g", "warn": "y", "plan": "d"}

# As três colunas da seção Tecnologias, na ordem em que aparecem.
# (status, subtítulo, classe CSS da coluna)
COLUNAS_TECNOLOGIA = [
    (Tecnologia.Status.APRENDI, "uso nos meus projetos", "learned"),
    (Tecnologia.Status.APRENDENDO, "estudo atual", "learning"),
    (Tecnologia.Status.QUERO, "próximos passos", "wish"),
]


def linhas_do_terminal(projetos):
    """Monta as linhas do "cat status.txt" a partir dos projetos cadastrados.

    Resultado, por exemplo:
        no ar ........... cpcc-agendamento
        planejamento .... curso-concurso, ia-ebd
    """
    linhas = []
    for valor, rotulo in Projeto.Status.choices:
        slugs = [p.slug for p in projetos if p.status == valor]
        if not slugs:
            continue
        pontos = "." * max(16 - len(rotulo), 3)  # alinha as colunas como no artefato
        cor = COR_NO_TERMINAL[Projeto.CORES_STATUS[valor]]
        linhas.append({"cor": cor, "texto": f"{rotulo} {pontos} {', '.join(slugs)}"})
    return linhas


def home(request):
    todos = list(Projeto.objects.all())

    colunas = []
    for status, subtitulo, classe in COLUNAS_TECNOLOGIA:
        colunas.append({
            "titulo": status.label,
            "subtitulo": subtitulo,
            "classe": classe,
            "itens": Tecnologia.objects.filter(status=status),
        })

    contexto = {
        # prefetch_related busca todos os prints numa consulta só
        "construidos": Projeto.objects.construidos().prefetch_related("prints"),
        "planejados": Projeto.objects.planejados(),
        "slugs": [p.slug for p in todos],
        "linhas_status": linhas_do_terminal(todos),
        "colunas_tecnologia": colunas,
        "experiencias": Experiencia.objects.all(),
        "formacoes": Formacao.objects.all(),
    }
    return render(request, "core/home.html", contexto)
