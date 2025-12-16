from django.contrib import admin
from .models import Livro

# Register your models here.

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'editora', 'ano_publicacao', 'categoria', 'status', 'data_cadastro']
    list_filter = ['editora', 'ano_publicacao', 'categoria', 'status', 'data_cadastro']
    search_fields = ['titulo', 'autor', 'categoria']
    readonly_fields = ['data_cadastro', 'data_atualizacao']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'autor', 'editora', 'ano_publicacao')
        }),
        ('Detalhes', {
            'fields': ('categoria', 'num_paginas', 'status', 'descricao', 'capa_url')
        }),
        ('Datas', {
            'fields': ('data_cadastro', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )
