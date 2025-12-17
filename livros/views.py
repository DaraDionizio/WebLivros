from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Livro

from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect

import json

# Create your views here.

def index(request):
    if request.method == 'POST':
        username = request.POST.get('login_user')
        password = request.POST.get('senha_user')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('livros:dashboard')
        else:
            return render(request, 'index.html', {
                'erro': 'Usuário ou senha inválidos'
            })

    return render(request, 'index.html')

@login_required(login_url='livros:index')
def dashboard(request):
    return render(request, 'dashboard.html')

# API Endpoints para gerenciar livros
@login_required
def listar_livros(request):
    """Retorna todos os livros em formato JSON"""
    livros = Livro.objects.all().values(
        'id', 'titulo', 'autor', 'editora', 'ano_publicacao', 
        'categoria', 'num_paginas', 'descricao', 'capa_url', 'status'
    )
    return JsonResponse(list(livros), safe=False)

def obter_livro(request, livro_id):
    """Retorna um livro específico em formato JSON"""
    livro = get_object_or_404(Livro, id=livro_id)
    data = {
        'id': livro.id,
        'titulo': livro.titulo,
        'autor': livro.autor,
        'editora': livro.editora,
        'ano_publicacao': livro.ano_publicacao,
        'categoria': livro.categoria,
        'num_paginas': livro.num_paginas,
        'descricao': livro.descricao,
        'capa_url': livro.capa_url,
        'status': livro.status,
    }
    return JsonResponse(data)

@login_required
@require_http_methods(["POST"])
def criar_livro(request):
    """Cria um novo livro"""
    try:
        data = json.loads(request.body)
        livro = Livro.objects.create(
            titulo=data.get('titulo'),
            autor=data.get('autor'),
            editora=data.get('editora'),
            ano_publicacao=data.get('ano_publicacao'),
            categoria=data.get('categoria'),
            num_paginas=data.get('num_paginas'),
            descricao=data.get('descricao', ''),
            capa_url=data.get('capa_url', ''),
            status=data.get('status', 'ativo'),
        )
        return JsonResponse({'id': livro.id, 'mensagem': 'Livro criado com sucesso!'}, status=201)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=400)

@login_required
@require_http_methods(["PUT", "PATCH"])
def atualizar_livro(request, livro_id):
    """Atualiza um livro existente"""
    try:
        livro = get_object_or_404(Livro, id=livro_id)
        data = json.loads(request.body)
        
        livro.titulo = data.get('titulo', livro.titulo)
        livro.autor = data.get('autor', livro.autor)
        livro.editora = data.get('editora', livro.editora)
        livro.ano_publicacao = data.get('ano_publicacao', livro.ano_publicacao)
        livro.categoria = data.get('categoria', livro.categoria)
        livro.num_paginas = data.get('num_paginas', livro.num_paginas)
        livro.descricao = data.get('descricao', livro.descricao)
        livro.capa_url = data.get('capa_url', livro.capa_url)
        livro.status = data.get('status', livro.status)
        livro.save()
        
        return JsonResponse({'mensagem': 'Livro atualizado com sucesso!'})
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=400)

@login_required
@require_http_methods(["DELETE"])
def deletar_livro(request, livro_id):
    """Deleta um livro"""
    try:
        livro = get_object_or_404(Livro, id=livro_id)
        livro.delete()
        return JsonResponse({'mensagem': 'Livro deletado com sucesso!'})
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=400)


def sair(request):
    logout(request)
    return redirect('livros:index')
