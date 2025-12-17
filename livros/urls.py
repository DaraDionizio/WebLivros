from django.urls import path
from . import views

app_name = 'livros'

urlpatterns = [
    # Páginas
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.sair, name='logout'),
    path('cadastrar/', views.cadastrar_usuario, name='cadastrar'),
    path('equipe/', views.equipe, name='equipe'),

    # API Endpoints
    path('api/livros/', views.listar_livros, name='listar_livros'),
    path('api/livros/<int:livro_id>/', views.obter_livro, name='obter_livro'),
    path('api/livros/criar/', views.criar_livro, name='criar_livro'),
    path('api/livros/<int:livro_id>/atualizar/', views.atualizar_livro, name='atualizar_livro'),
    path('api/livros/<int:livro_id>/deletar/', views.deletar_livro, name='deletar_livro'),
    
]
