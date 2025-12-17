
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

        progressItems: document.querySelectorAll('.progress-value')
    };
    
    console.log('Elementos do DOM carregados:', elementosDOM);
}

function renderizarDashboard() {
    try {
        // Validar se elementos do DOM existem antes de atualizar
        if (!elementosDOM.statTotal || !elementosDOM.statLidos || !elementosDOM.statLendo) {
            console.error('Elementos do DOM não encontrados');
            return;
        }

        // Atualizar estatísticas
        elementosDOM.statTotal.innerText = dadosLivros.total;
        elementosDOM.statLidos.innerText = dadosLivros.lidos;
        elementosDOM.statLendo.innerText = dadosLivros.lendo;
        elementosDOM.statEmprestimos.innerText = dadosLivros.emprestimosAtivos;

        // Calcular e atualizar progresso
        const totalProgresso = dadosLivros.lidos + dadosLivros.lendo + dadosLivros.queroLer;

        // Atualizar valores de progresso (Lido, Lendo, Quero Ler)
        const progressItems = document.querySelectorAll('.progress-value');
        if (progressItems[0]) progressItems[0].innerHTML = `<span>${dadosLivros.lidos}</span> de <span>${totalProgresso}</span>`;
        if (progressItems[1]) progressItems[1].innerHTML = `<span>${dadosLivros.lendo}</span> de <span>${totalProgresso}</span>`;
        if (progressItems[2]) progressItems[2].innerHTML = `<span>${dadosLivros.queroLer}</span> de <span>${totalProgresso}</span>`;

        console.log('Dashboard atualizado com sucesso');
    } catch (erro) {
        console.error('Erro ao renderizar dashboard:', erro);
    }
}

// Inicializar quando o DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        inicializarElementosDOM();
        renderizarDashboard();
    });
} else {
    inicializarElementosDOM();
    renderizarDashboard();
}

        console.log('Dashboard atualizado com sucesso');
    } catch (erro) {
        console.error('Erro ao renderizar dashboard:', erro);
    }
}

// Chamar ao carregar a página
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderizarDashboard);
} else {
    renderizarDashboard();
}