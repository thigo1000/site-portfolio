from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Projeto


def lista(request):
    """/projetos/ não tem página própria: manda pra seção de projetos da home."""
    return redirect(reverse("core:home") + "#projetos")


def detalhe(request, slug):
    projeto = get_object_or_404(Projeto.objects.prefetch_related("prints"), slug=slug)
    contexto = {
        "projeto": projeto,
        "outros": Projeto.objects.exclude(pk=projeto.pk),
    }
    return render(request, "projetos/detalhe.html", contexto)
