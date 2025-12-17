// Função para obter o CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

const dadosLivros = {
    total: 0,
    lidos: 0,
    lendo: 0,
    queroLer: 0,
    emprestimosAtivos: 0
};

let elementosDOM = {};

function inicializarElementosDOM() {
    elementosDOM = {
        statTotal: document.getElementById('stat-total'),
        statLidos: document.getElementById('stat-lidos'),
        statLendo: document.getElementById('stat-lendo'),
        statEmprestimos: document.getElementById('stat-emprestimos'),
        totalLivros: document.getElementById('total-livros'),
        livrosLista: document.getElementById('livros-lista'),
        btnNovoLivro: document.querySelector('.btn-novo-livro'),
        btnSalvarLivro: document.getElementById('btnSalvarLivro'),
        formLivro: document.getElementById('formLivro'),
        progressItems: document.querySelectorAll('.progress-value')
    };

    console.log('Elementos do DOM carregados:', elementosDOM);
}

function carregarLivros() {
    if (!window.API_URLS || !window.API_URLS.listar) {
        console.error('API URLs não definidas');
        return;
    }

    fetch(window.API_URLS.listar)
        .then(response => response.json())
        .then(livros => {
            console.log('Livros carregados:', livros);
            dadosLivros.total = livros.length;
            dadosLivros.lidos = livros.filter(l => l.status === 'lido').length;
            dadosLivros.lendo = livros.filter(l => l.status === 'lendo').length;
            dadosLivros.queroLer = livros.filter(l => l.status === 'quero_ler').length;
            dadosLivros.emprestimosAtivos = livros.filter(l => l.status === 'emprestado').length;
            atualizarDashboard();
            renderizarLivrosRecentes(livros);
        })
        .catch(erro => {
            console.error('Erro ao carregar livros:', erro);
        });
}

function renderizarDashboard() {
    try {
        if (!elementosDOM.statTotal) {
            console.error('Elementos do DOM não encontrados');
            return;
        }

        // Atualizar estatísticas
        elementosDOM.statTotal.innerText = dadosLivros.total;
        elementosDOM.statLidos.innerText = dadosLivros.lidos;
        elementosDOM.statLendo.innerText = dadosLivros.lendo;
        elementosDOM.statEmprestimos.innerText = dadosLivros.emprestimosAtivos;

        if (elementosDOM.totalLivros) {
            elementosDOM.totalLivros.innerText = `${dadosLivros.total} livros cadastrados`;
        }

        // Calcular e atualizar progresso
        const totalProgresso = dadosLivros.lidos + dadosLivros.lendo + dadosLivros.queroLer;

        const progressItems = document.querySelectorAll('.progress-value');
        if (progressItems[0]) progressItems[0].innerHTML = `<span>${dadosLivros.lidos}</span> de <span>${totalProgresso}</span>`;
        if (progressItems[1]) progressItems[1].innerHTML = `<span>${dadosLivros.lendo}</span> de <span>${totalProgresso}</span>`;
        if (progressItems[2]) progressItems[2].innerHTML = `<span>${dadosLivros.queroLer}</span> de <span>${totalProgresso}</span>`;

        console.log('Dashboard atualizado com sucesso');
    } catch (erro) {
        console.error('Erro ao renderizar dashboard:', erro);
    }
}

function atualizarDashboard() {
    renderizarDashboard();
}

function renderizarLivrosRecentes(livros) {
    if (!elementosDOM.livrosLista) return;

    if (livros.length === 0) {
        elementosDOM.livrosLista.innerHTML = `
            <i class="bi bi-book icon-placeholder"></i>
            <p>Nenhum livro cadastrado ainda</p>
            <button class="btn-novo-livro add-book-link">
                Adicionar primeiro livro
            </button>
        `;

        const btn = elementosDOM.livrosLista.querySelector('.btn-novo-livro');
        btn.addEventListener('click', abrirModalNovoLivro);
        
    } else {
        const livrosRecentes = livros.slice(0, 5);
        elementosDOM.livrosLista.innerHTML = livrosRecentes.map(livro => `
        <div class="livro-item d-flex align-items-center justify-content-between ${livro.status === 'emprestado' ? 'livro-emprestado' : ''}">


        
        <div class="d-flex align-items-center gap-2">
            <div class="livro-capa">
                ${
                    livro.capa_url
                        ? `<img src="${livro.capa_url}" alt="Capa do livro">`
                        : `<i class="bi bi-book capa-placeholder"></i>`
                }
            </div>

            <div class="livro-info">
                <h6 class="mb-0">${livro.titulo}</h6>
                <small class="text-muted">${livro.autor}</small>
            </div>
        </div>

        <button 
            class="btn btn-sm btn-danger"
            onclick="deletarLivro(${livro.id})"
            title="Excluir livro">
            <i class="bi bi-trash"></i>
        </button>

    </div>
`).join('');

    }
}

function abrirModalNovoLivro() {
    const modal = new bootstrap.Modal(document.getElementById('modalLivro'));
    modal.show();
}

function salvarLivro() {
    if (!window.API_URLS || !window.API_URLS.criar) {
        console.error('API URLs não definidas');
        return;
    }

    const dados = {
        titulo: document.getElementById('titulo').value,
        autor: document.getElementById('autor').value,
        editora: document.getElementById('editora').value,
        ano_publicacao: parseInt(document.getElementById('ano_publicacao').value),
        categoria: document.getElementById('categoria').value,
        num_paginas: parseInt(document.getElementById('num_paginas').value),
        descricao: document.getElementById('descricao').value,
        capa_url: document.getElementById('capa_url').value,
        status: document.getElementById('status').value,
    };
    if (dados.status === 'emprestado') {
        dados.emprestado_para = document.getElementById('emprestado_para').value;
        dados.data_emprestimo = document.getElementById('data_emprestimo').value;
    }

    fetch(window.API_URLS.criar, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(dados)
    })
        .then(response => response.json())
        .then(data => {
            console.log('Livro criado:', data);
            const modal = bootstrap.Modal.getInstance(document.getElementById('modalLivro'));
            modal.hide();
            elementosDOM.formLivro.reset();
            carregarLivros();
        })
        .catch(erro => {
            console.error('Erro ao salvar livro:', erro);
            alert('Erro ao salvar livro. Verifique os dados e tente novamente.');
        });
}

// Inicializar quando o DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
        inicializarElementosDOM();
        renderizarDashboard();
        carregarLivros();

        // Event listeners
        if (elementosDOM.btnNovoLivro) {
            elementosDOM.btnNovoLivro.addEventListener('click', abrirModalNovoLivro);
        }


        if (elementosDOM.btnSalvarLivro) {
            elementosDOM.btnSalvarLivro.addEventListener('click', salvarLivro);
        }
    });
} else {
    inicializarElementosDOM();
    renderizarDashboard();
    carregarLivros();

    // Event listeners
    if (elementosDOM.btnNovoLivro) {
        elementosDOM.btnNovoLivro.addEventListener('click', abrirModalNovoLivro);
    }

    if (elementosDOM.btnSalvarLivro) {
        elementosDOM.btnSalvarLivro.addEventListener('click', salvarLivro);
    }
    
}

const statusSelect = document.getElementById('status');
const camposEmprestimo = document.getElementById('campos-emprestimo');

statusSelect.addEventListener('change', () => {
    if (statusSelect.value === 'emprestado') {
        camposEmprestimo.style.display = 'block';
    } else {
        camposEmprestimo.style.display = 'none';

        // limpa os campos se mudar de ideia
        document.getElementById('emprestado_para').value = '';
        document.getElementById('data_emprestimo').value = '';
    }
});
