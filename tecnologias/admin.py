from django.contrib import admin

from .models import Tecnologia


@admin.register(Tecnologia)
class TecnologiaAdmin(admin.ModelAdmin):
    list_display = ("nome", "status", "descricao", "ordem")
    list_editable = ("status", "ordem")  # muda de coluna direto na lista, sem abrir o item
    list_filter = ("status",)
    search_fields = ("nome",)
