from .models import Perfil


def perfil(request):
    """Coloca o perfil em todos os templates (topo, rodapé e contato usam).

    Sem isso, cada view teria que buscar o perfil e passar no contexto.
    Está registrado em TEMPLATES > OPTIONS > context_processors no settings.py.
    """
    return {"perfil": Perfil.objects.first()}
