from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html

from .models import Print, Projeto


class PrintInline(admin.TabularInline):
    """Permite cadastrar os prints dentro da própria tela do projeto."""

    model = Print
    extra = 1
    fields = ("previa", "imagem", "legenda", "texto_alternativo", "mostrar_inteira", "ordem")
    readonly_fields = ("previa",)

    @admin.display(description="prévia")
    def previa(self, obj):
        if obj.pk and obj.imagem:
            return format_html('<img src="{}" style="height:60px;border-radius:4px">', obj.imagem.url)
        return "—"


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ("nome", "status", "ordem", "qtd_prints")
    list_editable = ("status", "ordem")
    list_filter = ("status",)
    search_fields = ("nome", "resumo", "problema")
    prepopulated_fields = {"slug": ("nome",)}  # preenche o slug enquanto você digita o nome
    inlines = [PrintInline]

    fieldsets = (
        (None, {"fields": ("nome", "slug", "status", "ordem")}),
        (
            "Projeto construído (no ar ou em deploy)",
            {"fields": ("resumo", "funcionalidades", "aprendizado", "proximo_passo")},
        ),
        (
            "Projeto em andamento ou planejamento",
            {
                "fields": ("problema", "meu_papel", "plano", "foco"),
                "description": "Só aparece no site o que estiver preenchido.",
            },
        ),
        ("Tecnologias e links", {"fields": ("stack", "url_site", "url_codigo", "codigo_privado")}),
    )

    def get_queryset(self, request):
        # Conta os prints numa consulta só, em vez de uma consulta por linha da lista
        return super().get_queryset(request).annotate(_qtd_prints=Count("prints"))

    @admin.display(description="prints", ordering="_qtd_prints")
    def qtd_prints(self, obj):
        return obj._qtd_prints
