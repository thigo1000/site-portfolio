# Portfólio · Thiago Limeira

Site pessoal em Django que funciona como currículo de desenvolvedor: projetos com prints, projetos em planejamento, tecnologias e trajetória. Todo o conteúdo é editado pelo admin do Django.

**Stack:** Python 3.12+ · Django 6.1 · SQLite · Pillow · python-dotenv · PythonAnywhere

## Estrutura

```
config/        configurações, URLs principais
core/          home, perfil (sobre mim e contato), experiência, formação
               + comando carregar_conteudo
projetos/      projetos, prints e página de cada projeto
tecnologias/   o que já aprendi, estou aprendendo e quero aprender
templates/     base.html (topo e rodapé de todas as páginas) e 404.html
static/        css/estilo.css e js/site.js
conteudo_inicial/prints/   prints usados pelo carregar_conteudo
```

## Rodar no computador (Windows, PowerShell)

```powershell
cd site-portfolio
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

copy .env.example .env
# abra o .env e cole uma SECRET_KEY gerada com:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

python manage.py migrate
python manage.py carregar_conteudo
python manage.py createsuperuser
python manage.py runserver
```

Site em http://127.0.0.1:8000 e admin em http://127.0.0.1:8000/admin

## Testes

```powershell
python manage.py test
```

## Deploy no PythonAnywhere

Conta grátis tem **um site por conta**. Como `adecin` e `cpcc` já estão em uso, crie uma conta nova (ex.: `thiagolimeira` → `thiagolimeira.pythonanywhere.com`).

1. Suba o projeto pro GitHub (o `.gitignore` já deixa de fora venv, `.env`, banco e uploads).
2. No PythonAnywhere, abra um **Bash console**:
   ```bash
   git clone https://github.com/thigo1000/site-portfolio.git
   cd site-portfolio
   mkvirtualenv --python=/usr/bin/python3.13 portfolio-venv
   pip install -r requirements.txt
   cp .env.example .env
   nano .env
   ```
   No `.env`: `SECRET_KEY` nova, `DEBUG=False`, `ALLOWED_HOSTS=SEUUSUARIO.pythonanywhere.com`. Salve com Ctrl+O, Enter, Ctrl+X.
3. Ainda no console:
   ```bash
   python manage.py migrate
   python manage.py collectstatic
   python manage.py carregar_conteudo
   python manage.py createsuperuser
   ```
4. Aba **Web** → *Add a new web app* → **Manual configuration** → **Python 3.13**.
5. **Virtualenv:** `portfolio-venv`
6. **Source code** e **Working directory:** `/home/SEUUSUARIO/site-portfolio`
7. **WSGI configuration file** (o link na aba Web): apague tudo e cole:
   ```python
   import os
   import sys

   path = "/home/SEUUSUARIO/site-portfolio"
   if path not in sys.path:
       sys.path.append(path)

   os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"

   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```
8. **Static files** (aba Web):

   | URL       | Directory                                   |
   |-----------|---------------------------------------------|
   | `/static/` | `/home/SEUUSUARIO/site-portfolio/staticfiles` |
   | `/media/`  | `/home/SEUUSUARIO/site-portfolio/media`       |

9. Em **Security**, ligue **Force HTTPS**.
10. Clique em **Reload** e abra o site.

### Atualizar o site depois

```bash
cd ~/site-portfolio
git pull
workon portfolio-venv
pip install -r requirements.txt     # só se mudou o requirements
python manage.py migrate            # só se mudou algum model
python manage.py collectstatic      # só se mudou CSS, JS ou imagem do static
```
Depois, **Reload** na aba Web. Texto, projeto, print e foto se mudam pelo admin, sem deploy.
