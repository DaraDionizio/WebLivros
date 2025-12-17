from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Livro(models.Model):
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('lendo', 'Lendo Agora'),
        ('lido', 'Lido'),
        ('emprestado', 'Emprestado'),
        ('quero_ler', 'Quero Ler'),
    ]
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='livros',
        verbose_name='Usuário'
    )

    titulo = models.CharField(max_length=200, verbose_name='Título')
    autor = models.CharField(max_length=200, verbose_name='Autor')
    editora = models.CharField(max_length=200, verbose_name='Editora')
    ano_publicacao = models.IntegerField(verbose_name='Ano de Publicação')
    categoria = models.CharField(max_length=100, verbose_name='Categoria/Gênero', default='Não categorizado')
    num_paginas = models.IntegerField(verbose_name='Número de Páginas')
    descricao = models.TextField(verbose_name='Descrição', blank=True)
    capa_url = models.URLField(verbose_name='URL da Capa', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo', verbose_name='Status')
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')


    emprestado_para = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    data_emprestimo = models.DateField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.titulo} - {self.autor}"
    class Meta:
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'
        ordering = ['-data_cadastro']
