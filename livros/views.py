from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Livro
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib import messages

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
    livros = Livro.objects.filter(usuario=request.user).values(
        'id', 'titulo', 'autor', 'editora', 'ano_publicacao', 
        'categoria', 'num_paginas', 'descricao', 'capa_url', 'status'
    )
    return JsonResponse(list(livros), safe=False)


@login_required
def obter_livro(request, livro_id):
    livro = get_object_or_404(
        Livro,
        id=livro_id,
        usuario=request.user
    )

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
        'emprestado_para': livro.emprestado_para,
        'data_emprestimo': livro.data_emprestimo,
    }

    return JsonResponse(data)


@login_required
@require_http_methods(["POST"])
def criar_livro(request):
    try:
        data = json.loads(request.body)

        status = data.get('status', 'ativo')

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
            usuario=request.user,

            emprestado_para=data.get('emprestado_para') if status == 'emprestado' else None,
            data_emprestimo=data.get('data_emprestimo') if status == 'emprestado' else None,
        )

        return JsonResponse(
            {'id': livro.id, 'mensagem': 'Livro criado com sucesso!'},
            status=201
        )

    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=400)


@login_required
@require_http_methods(["POST", "PUT"])
def atualizar_livro(request, livro_id):
    print(">>> ATUALIZAR LIVRO CHAMADO <<<", livro_id)
    try:
        livro = get_object_or_404(
            Livro,
            id=livro_id,
            usuario=request.user
        )

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

        # empréstimo
        if livro.status == 'emprestado':
            livro.emprestado_para = data.get('emprestado_para')
            livro.data_emprestimo = data.get('data_emprestimo')
        else:
            livro.emprestado_para = None
            livro.data_emprestimo = None

        livro.save()

        return JsonResponse({'mensagem': 'Livro atualizado com sucesso!'})

    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=400)



@login_required
@require_http_methods(["DELETE"])
def deletar_livro(request, livro_id):
    """Deleta um livro"""
    try:
        livro = get_object_or_404(
    Livro,
    id=livro_id,
    usuario=request.user
)

        livro.delete()
        return JsonResponse({'mensagem': 'Livro deletado com sucesso!'})
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=400)


def sair(request):
    logout(request)
    return redirect('livros:index')


def cadastrar_usuario(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Usuário já existe")
            return redirect("livros:cadastrar")

        User.objects.create_user(
            username=username,
            password=password
        )

        messages.success(request, "Usuário criado com sucesso!")
        return redirect("livros:index")

    return render(request, "cadastrar.html")

def equipe(request):
    return render(request, 'equipe.html')

