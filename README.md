# 🎮 Catálogo de Jogos Digitais

Sistema de linha de comando (CLI) e gerenciamento de catálogo pessoal de jogos digitais desenvolvido como **miniprojeto** prático para a disciplina de Programação Orientada a Objetos (POO) do semestre 2026.2 do curso de Engenharia de Software da Universidade Federal do Cariri (UFCA).

---

## 📌 Descrição e Objetivo

O **Catálogo de Jogos Digitais** é uma aplicação voltada para o gerenciamento e acompanhamento de acervos de jogos. O sistema permite cadastrar novos títulos, registrar o progresso de jogatina (horas jogadas e status de conclusão), categorizar os jogos por coleções personalizadas e gerar relatórios estatísticos detalhados sobre o desempenho do jogador.

### Principais Funcionalidades:
- **CRUD de Jogos:** Cadastro, leitura, atualização de progresso e exclusão de jogos.
- **Diferenciação por Tipo de Experiência:** Suporte a jogos de Campanha, Competitivos e Cooperativos.
- **Gestão de Progresso:** Regras de negócio rigorosas para alteração de status, validação de horas jogadas e avaliações.
- **Coleções Personalizadas:** Organização de jogos em listas customizadas (ex: *Favoritos*, *Zerados 2026*).
- **Relatórios Estatísticos:** Métricas de tempo total jogado, média de avaliações, top 5 mais jogados e percentuais de status.
- **Persistência de Dados:** Salvamento em arquivos JSON.
- **Emissão de aviso:** Aparece ao exibir configurações caso os jogos finalizados estejam abaixo da meta.

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
├── cli.py                                  # Interface de subcomandos (parsers)
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

### 1. Clone o repositório e acesse a pasta raiz do projeto

```bash
git clone https://github.com/kaue-aps/CatalogoJogosDigitais.git
cd CatalogoJogosDigitais
```

### 2. Crie e ative um ambiente virtual (Recomendado)

Isola as dependências e evita conflitos com bibliotecas já instaladas no sistema

```bash
python -m venv .venv
```

#### No Windows:
```bash
.venv\Scripts\activate
```
#### No Linux/macOS:
```bash
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Para executar os testes automatizados

Use `-v` para exibição detalhada:
```bash
python -m pytest -v
```

## 💻 Exemplos de execução dos subcomandos

Execute os comandos na raiz do projeto. Os IDs são atribuídos automaticamente ao cadastrar jogos, coleções e usuários; substitua os valores de exemplo pelos IDs existentes no seu catálogo.

### Jogos

```bash
# Cadastrar jogos de cada categoria
python main.py jogos cadastrar --titulo "Hades" --genero "Rogue-like" --plataforma "PC"
python main.py jogos cadastrar --titulo "Hollow Knight" --genero "Aventura" --plataforma "PC" --tipo campanha --capitulos-totais 20
python main.py jogos cadastrar --titulo "Valorant" --genero "FPS" --plataforma "PC" --tipo competitivo
python main.py jogos cadastrar --titulo "It Takes Two" --genero "Aventura" --plataforma "Console" --tipo cooperativo --max-jogadores 2

# Listar, buscar e ordenar jogos
python main.py jogos listar
python main.py jogos buscar --titulo "Hollow"
python main.py jogos buscar --genero "FPS"
python main.py jogos buscar --status "JOGANDO"
python main.py jogos buscar --plataforma "PC"
python main.py jogos ordenar --por avaliacao
python main.py jogos ordenar --por horas --crescente

# Registrar progresso, avaliar e remover um jogo
python main.py jogos registrar-progresso --id 1 --horas 2.5
python main.py jogos avaliar --id 1 --nota 9.0
python main.py jogos deletar --id 1
```

### Jogos de campanha

```bash
python main.py jogos-campanha avancar-capitulo --id 2 --capitulos 3
python main.py jogos-campanha percentual_conclusao --id 2
```

### Jogos competitivos

```bash
python main.py jogos-competitivo atualizar-ranking --id 3 --novo_ranking "Gold"
python main.py jogos-competitivo registrar-partida --id 3 --resultado "VITÓRIA"
python main.py jogos-competitivo registrar-partida --id 3 --resultado "DERROTA"
python main.py jogos-competitivo taxa-vitoria --id 3
```

### Jogos cooperativos

```bash
python main.py jogos-cooperativo adicionar-participante --id 4 --nome "Ana"
python main.py jogos-cooperativo registrar-sessao --id 4
```

### Coleções

```bash
python main.py colecoes criar --nome "Favoritos"
python main.py colecoes deletar --id 1
```


### Relatórios

```bash
python main.py relatorio --tipo total-jogos
python main.py relatorio --tipo total-horas
python main.py relatorio --tipo top5-mais-jogados
python main.py relatorio --tipo percentual-por-status
python main.py relatorio --tipo media-avaliacao
```

### Configurações

```bash
python main.py config exibir
python main.py config redefinir --meta-anual 20
python main.py config redefinir --plataforma-principal PC
python main.py config redefinir --limite-andamento 4
python main.py config redefinir --generos-favoritos RPG Aventura Estratégia
```

### Usuários

```bash
python main.py usuarios cadastrar --nome "jogador1"
python main.py usuarios listar
python main.py usuarios adicionar-colecao --id-colecao 1 --id-usuario 1
python main.py usuarios remover-colecao --id-colecao 1 --id-usuario 1
python main.py usuarios deletar --id 1
python main.py usuarios listar-colecoes --id
python main.py usuarios resumo --id
```

