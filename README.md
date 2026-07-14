# 🎮 Sistema de Gamificação

## 📖 Sobre o projeto

Este é um projeto de gamificação voltado para empresas.

A ideia é simples: funcionários que cumprem tarefas, mantêm disciplina e atingem metas recebem moedas como recompensa. Essas moedas podem ser utilizadas para resgatar produtos e benefícios disponíveis na loja da plataforma.

O projeto ainda está em desenvolvimento e novas funcionalidades serão adicionadas conforme ele evolui.

> **Observação:** utilizei IA como ferramenta de apoio durante o desenvolvimento, principalmente para HTML, CSS e JavaScript. Toda a lógica da aplicação, estrutura do sistema, modelagem do banco e implementação em Django foram desenvolvidas por mim.

---

## 🌐 Acesse o projeto

👉 https://gamificacao-obk4.onrender.com/

---

## 🛠 Tecnologias utilizadas

- Python
- Django
- PostgreSQL
- psycopg2-binary
- HTML
- CSS
- JavaScript

---

## 📌 Funcionalidades

### 📊 Dashboard

Área inicial do colaborador, onde é possível visualizar:

- saldo de moedas;
- histórico de atividades;
- progresso dentro da plataforma.

---

### ✅ Tarefas

As tarefas são divididas em três níveis de dificuldade:

- Fácil
- Média
- Difícil

As tarefas difíceis precisam passar por aprovação antes da recompensa ser liberada.

Cada colaborador também possui uma organização das tarefas por status:

- Disponíveis
- Em revisão
- Rejeitadas
- Concluídas

---

### 🛒 Loja

Os colaboradores podem trocar moedas por diferentes recompensas, como:

- roupas;
- eletrônicos;
- vales;
- outros benefícios.

A interface muda dinamicamente conforme:

- quantidade de moedas do usuário;
- disponibilidade em estoque.

---

### 🏆 Ranking

Atualmente está desativado.

A ideia é exibir rankings como:

- melhores colaboradores;
- melhores departamentos;
- outros indicadores de desempenho.

---

### 📈 Relatórios

Permite acompanhar informações da empresa e dos colaboradores, como:

- histórico de prêmios;
- resgates realizados;
- análises gerais.

Também é possível exportar os dados em **CSV**.

---

### 👤 Perfil

Área destinada às informações pessoais do colaborador.

Também funciona como um histórico dos prêmios já conquistados.

---

### ⚙ Configurações

As funcionalidades variam conforme o tipo de usuário.

**Funcionário**

- alterar senha;
- gerenciar informações da conta.

**Administrador**

- aprovar ou rejeitar tarefas;
- cadastrar colaboradores;
- cadastrar produtos;
- cadastrar tarefas;
- visualizar informações gerais do sistema.

---

## 🚀 Próximas melhorias

- Sistema de ranking completo
- Conquistas e medalhas
- Notificações
- Dashboard com mais gráficos
- Melhorias na responsividade
- Novos relatórios
- Mais opções de recompensas

---

## 💡 Objetivo

Este projeto foi criado para praticar desenvolvimento web utilizando Django, além de explorar conceitos de gamificação, autenticação, permissões, banco de dados, geração de relatórios e organização de um sistema com múltiplos módulos.
