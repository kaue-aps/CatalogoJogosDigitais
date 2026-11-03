# 🎮 Catálogo de Jogos Digitais

Sistema de linha de comando (CLI) e gerenciamento de catálogo pessoal de jogos digitais desenvolvido como **miniprojeto** prático para a disciplina de Programação Orientada a Objetos (POO) do semestre 2026.2 do curso de Engenharia de Software da Universidade Federal do Cariri (UFCA).

---

## 📌 Descrição e Objetivo

O **Catálogo de Jogos Digitais** é uma aplicação voltada para o gerenciamento e acompanhamento de acervos de jogos. O sistema permite cadastrar novos títulos, registrar o progresso de jogatina (horas jogadas e status de conclusão), categorizar os jogos por coleções personalizadas e gerar relatórios estatísticos detalhados sobre o desempenho do jogador.

### Principais Funcionalidades Planejadas:
- **CRUD de Jogos:** Cadastro, leitura, atualização de progresso e exclusão de jogos.
- **Diferenciação por Tipo de Experiência:** Suporte a jogos de Campanha, Competitivos e Cooperativos.
- **Gestão de Progresso:** Regras de negócio rigorosas para alteração de status, validação de horas jogadas e avaliações.
- **Coleções Personalizadas:** Organização de jogos em listas customizadas (ex: *Favoritos*, *Zerados 2026*).
- **Relatórios Estatísticos:** Métricas de tempo total jogado, média de avaliações, top 5 mais jogados e percentuais de status.
- **Persistência de Dados:** Salvamento em arquivos JSON.

---

## 🏗️ Estrutura de Classes

Abaixo consta um resumo simplificado das classes empregadas no projeto. Informações mais detalhadas sobre cada classe podem ser encontradas no [Diagrama de Classes UML](docs/diagrama_classes_uml.md).

- Jogo
- JogoCampanha (Herda de Jogo)
- JogoCooperativo (Herda de Jogo)
- JogoCompetitivo (Herda de Jogo)
- Colecao (Agregação de Jogos)
- Usuario (Agregação de Coleções)

---

## 📂 Decisões de Design

O miniprojeto seguiu uma arquitetura em camadas, isolando as responsabilidades e facilitando a manutenção do código:

- Base de dados em JSON: `data/`
- Documentação técnica: `docs/`
- Classes de domínio (modelos): `src/models/`
- Ponte para persistência de dados: `src/repositories`
- Serviços para o ponto de entrada: `src/services`
- Testes unitários e de integração: `testes/`


```
🕹️ CatalogoJogosDigitais/
│
├── data/                                  # Dados e configurações
│   ├── catalogo.json                      # Base de dados principal (criada durante a execução do sistema)
│   └── settings.json                      # Configurações predefinidas do sistema e preferências do usuário
│
├── docs/                                  # Documentação técnica
│   └── diagrama_classes_uml.md            # Diagrama das classes de domínio em mermaid.js
│
├── src/                                   # Código-fonte da aplicação
│   ├── models/                            # Entidades do domínio
│   │   ├── __init__.py
│   │   ├── categorias.py
│   │   ├── colecao.py
│   │   ├── jogo.py
│   │   └── usuario.py
│   │
│   ├── repositories/                      # Persistência e configuração desacoplados
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── persistencia.py
│   │
│   └── services/                          # Regras de negócio e operações
│       ├── __init__.py
│       ├── colecao_service.py
│       ├── configuracao_service.py
│       ├── jogos_service.py
│       ├── relatorio_service.py
│       └── usuario_service.py
│
├── testes/                                 # Testes automatizados com pytest
│   ├── testes_integracao/
│   │   ├── __init__.py
│   │   └── test_regras_de_negocio.py
│   │
│   └── testes_unitarios/
│       ├── __init__.py
│       ├── test_categorias.py
│       ├── test_colecao.py
│       ├── test_jogo.py
│       └── test_usuario.py
│
├── .gitignore
├── main.py                                 # Ponto de entrada CLI
├── README.md                               # Documentação do projeto
└── requirements.txt                        # Dependências externas
```

---

## 🧪 Cobertura de Testes


1. Os **testes unitários** abrangem a criação e a manipulação de objetos das **classes de domínio**:

- Criação validada de Jogos (e suas subclasses), Colecoes e Usuarios
- Erros ao violar regras lógicas e relacionais (Ex: duplicidade, valores fora do intervalo)
- Alteração de status do jogo ao registrar progresso, finalizar ou reiniciar
- Finalização e avaliação do jogo quando permitido
- Registro de data de início e data de término do jogo
- Cálculo de atributos derivados (JogoCampanha e JogoCompetitivo)
- Inclusão e remoção de Colecoes de um Usuario


2. Os **testes de integração** concentram-se nas **regras de negócio**, que por sua vez necessitam da atuação simultânea de outras partes do código. Os testes abrangem:

- Proibição de criar jogos duplicados (critério definido no método \_\_eq\_\_)
- Avaliação somente após finalização do jogo
- Persistência progressiva de horas jogadas ao registrar progresso
- Emissão de aviso caso o número de jogos finalizados seja inferior à meta anual
- Limitação de jogos com status "JOGANDO"


🚩 Foram realizados mais de 30 funções de teste, ultrapassando o mínimo estabelecido no pdf.

---

## 📝 Requisitos de POO atentidos pelo projeto

Além da modelagem e herança acima explicados, o projeto contempla:

#### Encapsulamento e validações

- `@property` para validação de **nota de avaliação** (0-10), **horas jogadas** >= 0 e definição de **título não vazio** no âmbito da [classe Jogo](src/models/jogo.py)
- Validação indireta da alteração de status e avanço de progresso por meio de métodos de instância convencionais

#### Métodos especiais

Foram implementados nas seguintes classes:

- Jogo: `__str__`, `__repr__`, `__eq__`, `__lt__` (exigidos no material)
- Colecao: `__str__`, `__eq__` (igualdade com base no nome e mesmos jogos), `__gt__` (comparação com base na quantidade de jogos incluídos)
- Usuario: `__str__`, `__repr__`

#### Persistência

A persistência em JSON foi feita usando dois módulos (ou duas classes): um para **configurações** e outro para os dados do **catálogo** em si:

- CatalogoJSON: contém método de leitura e salvamento (arquivo `catalogo.json`)
- ConfiguracaoJSON: contém método de leitura e salvamento (arquvio `settings.json`)

Tais classes não são dotadas de especialização, elas só gravam dados genéricos. A especialização é delegada aos módulos de serviço.

> Os módulos de serviço viabilizam a leitura/escrita através dos métodos de serialização (`to_dict()`) e desserialização (`from_dict()`) definidos nas próprias classes de domínio

## 🔨 Instruções de Execução