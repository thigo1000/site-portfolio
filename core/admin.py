from django.contrib import admin
from django.utils.html import format_html

from .models import Experiencia, Formacao, Perfil

# Textos do topo do admin
admin.site.site_header = "Portfólio · administração"
admin.site.site_title = "Portfólio"
admin.site.index_title = "O que você quer atualizar?"


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Topo do site", {"fields": ("nome", "cargo", "cidade")}),
        ("Sobre mim", {"fields": ("titulo_sobre", "sobre", "destaques", "foto", "previa_foto")}),
        ("Contato", {"fields": ("email", "github_url", "linkedin_url", "texto_contato")}),
    )
    readonly_fields = ("previa_foto",)

    @admin.display(description="foto atual")
    def previa_foto(self, obj):
        if obj.foto:
            return format_html('<img src="{}" style="max-height:160px;border-radius:8px">', obj.foto.url)
        return "Nenhuma foto enviada ainda"

    # Só pode existir um perfil: o botão "Adicionar" some depois do primeiro
    def has_add_permission(self, request):
        return not Perfil.objects.exists()

    # E ele não pode ser apagado pelo admin (o site depende dele)
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Experiencia)
class ExperienciaAdmin(admin.ModelAdmin):
    list_display = ("cargo", "empresa", "periodo", "ordem")
    list_editable = ("ordem",)


@admin.register(Formacao)
class FormacaoAdmin(admin.ModelAdmin):
    list_display = ("curso", "instituicao", "periodo", "ordem")
    list_editable = ("ordem",)
