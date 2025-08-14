from django.contrib import admin
from .models import Avaliacao

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'nota', 'criado_em',)
    search_fields = ('nome',)
    list_filter = ('nota',)
