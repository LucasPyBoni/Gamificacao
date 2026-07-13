## Sobre o projeto:

Projeto baseado em gamificação, onde os funcionários que cumprem tarefas e são disciplinados recebem moedas, e em troca, podem reivindicar prêmios na loja.
Ainda em evolução e com muitas funcionalidades a vir pela frente.

OBS: Foi feita com ajuda de IA, principalmente o HTML/CSS e JS

### Link do site
[Gamificação](https://gamificacao-obk4.onrender.com/)

### Principais Bibliotecas:

Framework Django, psycopg2-binary para o banco de dados 

### Divisões: 

. dashboard - Onde o funcionário vê o saldo, histórico de atividades e suas progressões.

. tarefas - Tarefas divididas em fácil, média e difícil. As dificeis precisam passar por revisão, pois pagam muito, além disso, tem uma divisão entre disponiveis, em revisão, rejeitadas e concluidas para cada colaborador

. loja - Roupas, eletrônicos, Vales e outros. Os campos mudam se o funcionário tem pouca moeda ou se o estoque do produto está zerado.

. ranking - Está inativo por enquanto, mas aqui vai ter uma ranking dos melhores funcionários ou departamentos.

. relatórios - Dados sobre o histórico do funcionário ou da empresa em relação aos prêmios, podendo exportar csv para melhor análise.

. perfil - Aqui é onde fica as informações pessoais e estão guardadas os prêmios do colaborador.

. configurações - Se for funcionário normal, aqui é onde troca senha, se for admin, é onde aprova ou rejeita as tarefas, visualiza todos os dados e cadastra produtos, tarefas e trabalhadores.
