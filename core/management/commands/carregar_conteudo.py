"""
Comando: python manage.py carregar_conteudo

Preenche um banco VAZIO com o conteúdo aprovado no artefato: perfil,
experiências, formações, projetos (com os prints) e tecnologias.

Serve pra duas coisas:
1. Você não precisa digitar tudo no admin na primeira vez.
2. No PythonAnywhere o banco começa vazio (o db.sqlite3 não vai pro GitHub),
   então é só rodar o comando lá também.

Depois disso, qualquer mudança é feita pelo admin.
"""

from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.models import Experiencia, Formacao, Perfil
from projetos.models import Print, Projeto
from tecnologias.models import Tecnologia

PASTA_PRINTS = Path(settings.BASE_DIR) / "conteudo_inicial" / "prints"

PERFIL = {
    "nome": "Thiago Limeira de Oliveira",
    "cargo": "Desenvolvedor Python · Django",
    "cidade": "Rio de Janeiro",
    "titulo_sobre": "De quem atende para quem constrói",
    "sobre": (
        "Sou formado em Análise e Desenvolvimento de Sistemas e passei os últimos anos "
        "trabalhando com atendimento ao público. Foi ali que aprendi a ouvir quem usa um "
        "serviço e entender o que realmente precisa ser resolvido.\n\n"
        "Hoje levo isso pro código. Comecei com um sistema de cadastro em linha de comando "
        "e cheguei a dois sistemas em Django usados por pessoas de verdade: o site de uma "
        "igreja, com área de membros e cursos em vídeo, e um app de agendamento para os "
        "moradores de um condomínio, com regras que foram mudando conforme o uso.\n\n"
        "Gosto de escrever o código eu mesmo e entender cada parte do que faço. Meu objetivo "
        "agora é a primeira vaga como desenvolvedor."
    ),
    "destaques": "ADS · Estácio\nPython · Django\nRio de Janeiro · RJ",
    "email": "thigooliveira781th@gmail.com",
    "github_url": "https://github.com/thigo1000",
    "linkedin_url": "https://www.linkedin.com/in/thiago-limeira/",
    "texto_contato": (
        "Estou em busca da primeira vaga como desenvolvedor. Se quiser falar sobre um "
        "projeto ou uma oportunidade, me chama."
    ),
}

EXPERIENCIAS = [
    {"cargo": "Porteiro", "empresa": "Condomínio Presidente Carlos de Campos", "periodo": "09/2025 – atual"},
    {
        "cargo": "Garçom no setor de nutrição",
        "empresa": "Rede D'Or São Luiz · Copa Star · promovido de Auxiliar de Governança",
        "periodo": "até 01/2025",
    },
    {"cargo": "Atendimento e varejo", "empresa": "Americanas · Assaí · Viação Pavunense", "periodo": "anteriormente"},
]

FORMACOES = [
    {
        "curso": "Análise e Desenvolvimento de Sistemas",
        "instituicao": "Estácio · Graduação tecnológica",
        "periodo": "07/2020 – 12/2022",
    },
    {"curso": "Técnico em Administração", "instituicao": "Senac RJ", "periodo": "2018"},
]

PROJETOS = [
    {
        "nome": "Site da ADECIN",
        "slug": "site-adecin",
        "status": Projeto.Status.EM_DEPLOY,
        "resumo": (
            "Site oficial da ADECIN Nova Jerusalém, com área pública e área de membros. "
            "Começou como projeto de estudo com uma igreja fictícia e virou o site real."
        ),
        "funcionalidades": (
            "Carrossel de avisos na home, atualizado pelo admin\n"
            "Agenda, álbuns de fotos e vídeos, páginas de PGM e EBD\n"
            "Cursos e treinamentos em vídeo para os membros\n"
            "Login nativo do Django, com cadastro e recuperação de senha\n"
            "Envio de várias fotos de uma vez pelo admin"
        ),
        "aprendizado": (
            "Configurar arquivos estáticos e de mídia em produção, resolver erro 404 causado "
            "por caracteres especiais em nomes de arquivo e apresentar o sistema para o pastor, "
            "ajustando a partir do retorno dele."
        ),
        "stack": "Python, Django, SQLite, Pillow, PythonAnywhere",
        "url_site": "https://adecin.pythonanywhere.com",
        "url_codigo": "https://github.com/thigo1000/site-adecin",
        "prints": [
            ("adecin-home.jpg", "início", "Página inicial do site da ADECIN com carrossel de avisos", False),
            ("adecin-cursos.jpg", "cursos", "Página de Cursos e Treinamentos do site da ADECIN", False),
        ],
    },
    {
        "nome": "Agendamento de massagem",
        "slug": "cpcc-agendamento",
        "status": Projeto.Status.NO_AR,
        "resumo": (
            "Sistema de agendamento do espaço de massagem de um condomínio com 2 blocos e "
            "84 apartamentos, usado pelos moradores e pela administração."
        ),
        "funcionalidades": (
            "Login por apartamento, no formato bloco-apartamento\n"
            "Administração lança os horários de cada massagista por data\n"
            "O sistema bloqueia horários que se sobrepõem, porque a sala é uma só\n"
            "Uma sessão de 30 minutos por semana para cada apartamento\n"
            "Agenda da semana seguinte liberada a partir de sexta-feira\n"
            "Massagistas com conta própria, só para ver os horários delas"
        ),
        "proximo_passo": "Reserva do salão de festas e da churrasqueira no mesmo sistema.",
        "stack": "Python, Django, Auth, SQLite, PythonAnywhere",
        "url_site": "https://cpcc.pythonanywhere.com",
        "codigo_privado": True,
        "prints": [
            ("cpcc-disponibilidade.jpg", "disponibilidade", "Tela de disponibilidade do sistema de agendamento", True),
            ("cpcc-login.jpg", "login", "Tela de login do sistema de agendamento de massagem", False),
        ],
    },
    {
        "nome": "Implantação de sistema de gestão do condomínio",
        "slug": "gestao-condominio",
        "status": Projeto.Status.EM_ANDAMENTO,
        "problema": "O condomínio precisa de um sistema de gestão com suporte 24 horas, contratado de uma empresa.",
        "meu_papel": (
            "Levantar o que o condomínio precisa, comparar fornecedores, organizar e migrar os "
            "dados do condomínio e fazer a ponte entre o síndico e a empresa."
        ),
        "foco": "Requisitos e migração de dados",
    },
    {
        "nome": "Site de curso para concurso",
        "slug": "curso-concurso",
        "status": Projeto.Status.PLANEJAMENTO,
        "problema": (
            "Um professor quer vender videoaulas para concurso sem perder boa parte do lucro "
            "em taxas de plataforma."
        ),
        "plano": (
            "Site próprio com assinatura e pagamento recorrente, vídeos em serviço de streaming. "
            "O professor cria as aulas, eu cuido do site e da divulgação."
        ),
        "stack": "Site próprio, Asaas, Panda Video ou Bunny, Hostinger",
    },
    {
        "nome": "IA para a Escola Bíblica Dominical",
        "slug": "ia-ebd",
        "status": Projeto.Status.PLANEJAMENTO,
        "problema": "Alunos da EBD têm dúvidas entre uma aula e outra e nem sempre têm a quem perguntar.",
        "plano": "Assistente que responde dúvidas com base nos ensinamentos da igreja, pensado para os alunos.",
        "stack": "Python, Django, API de IA",
    },
    {
        "nome": "Blog informativo com afiliados",
        "slug": "blog-afiliados",
        "status": Projeto.Status.PLANEJAMENTO,
        "problema": "Gerar renda com conteúdo útil mantendo o custo de domínio e hospedagem baixo.",
        "plano": "Blog de conteúdo informativo monetizado com links de afiliados e anúncios.",
        "foco": "Conteúdo, SEO e custo baixo",
    },
]

# (nome, descrição, status)
TECNOLOGIAS = [
    ("Python", "Orientação a objetos, JSON, sistemas em linha de comando", Tecnologia.Status.APRENDI),
    (
        "Django",
        "Models e ORM, migrations, views, templates, forms, admin customizado, login e recuperação de senha",
        Tecnologia.Status.APRENDI,
    ),
    ("SQLite", "Banco dos meus projetos em Django", Tecnologia.Status.APRENDI),
    ("HTML e CSS", "Templates e páginas dos sistemas", Tecnologia.Status.APRENDI),
    ("Git e GitHub", "Versionamento e repositórios", Tecnologia.Status.APRENDI),
    ("Deploy", "PythonAnywhere, variáveis de ambiente, arquivos estáticos e de mídia", Tecnologia.Status.APRENDI),
    ("Django", "Aprofundando o que já uso", Tecnologia.Status.APRENDENDO),
    ("Django REST Framework", "Construção de APIs", Tecnologia.Status.APRENDENDO),
    ("PostgreSQL", "Já usei uma vez, quero tornar padrão", Tecnologia.Status.APRENDENDO),
    ("JavaScript", "Mais controle no front dos sites", Tecnologia.Status.QUERO),
    ("Testes automatizados", "Para mexer em sistemas no ar com segurança", Tecnologia.Status.QUERO),
    ("Integração com IA", "Base para a IA da EBD", Tecnologia.Status.QUERO),
    ("Automação", "Tarefas repetitivas resolvidas com código", Tecnologia.Status.QUERO),
    ("Power BI", "Análise e visualização de dados", Tecnologia.Status.QUERO),
    ("Cibersegurança", "Proteger os sistemas que construo", Tecnologia.Status.QUERO),
]


class Command(BaseCommand):
    help = "Preenche um banco vazio com o conteúdo inicial do portfólio."

    def handle(self, *args, **options):
        # Proteção: se já tem conteúdo, não mexe. Assim o comando nunca apaga
        # nem sobrescreve o que você editou pelo admin.
        if Perfil.objects.exists() or Projeto.objects.exists():
            raise CommandError(
                "O banco já tem conteúdo. Esse comando é só para banco vazio; "
                "para mudar textos, use o admin."
            )

        # atomic: ou salva tudo, ou não salva nada (se der erro no meio, desfaz)
        with transaction.atomic():
            Perfil.objects.create(**PERFIL)

            for ordem, dados in enumerate(EXPERIENCIAS, start=1):
                Experiencia.objects.create(ordem=ordem, **dados)

            for ordem, dados in enumerate(FORMACOES, start=1):
                Formacao.objects.create(ordem=ordem, **dados)

            for ordem, dados in enumerate(PROJETOS, start=1):
                dados = dict(dados)  # cópia, pra não alterar a lista original
                prints = dados.pop("prints", [])
                projeto = Projeto.objects.create(ordem=ordem, **dados)
                for ordem_print, (arquivo, legenda, alt, inteira) in enumerate(prints, start=1):
                    self.criar_print(projeto, arquivo, legenda, alt, inteira, ordem_print)

            for ordem, (nome, descricao, status) in enumerate(TECNOLOGIAS, start=1):
                Tecnologia.objects.create(nome=nome, descricao=descricao, status=status, ordem=ordem)

        self.stdout.write(self.style.SUCCESS(
            f"Pronto: 1 perfil, {len(EXPERIENCIAS)} experiências, {len(FORMACOES)} formações, "
            f"{len(PROJETOS)} projetos, {Print.objects.count()} prints e {len(TECNOLOGIAS)} tecnologias."
        ))

    def criar_print(self, projeto, arquivo, legenda, alt, inteira, ordem):
        caminho = PASTA_PRINTS / arquivo
        if not caminho.exists():
            raise CommandError(f"Print não encontrado: {caminho}")
        item = Print(
            projeto=projeto,
            legenda=legenda,
            texto_alternativo=alt,
            mostrar_inteira=inteira,
            ordem=ordem,
        )
        # .save() do ImageField copia o arquivo pra pasta media/projetos/ e salva o registro
        with caminho.open("rb") as f:
            item.imagem.save(arquivo, File(f), save=True)
