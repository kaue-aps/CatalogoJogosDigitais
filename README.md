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
- **Persistência de Dados:** Salvamento em arquivos JSON ou banco SQLite.

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
- Testes unitários e de integração: `tests/`


```
🕹️ CatalogoJogosDigitais/
│
├── data/                                 # Arquivos de dados persistidos
│   ├── catalogo.json                     # Base de dados unificada (usuários, coleções e jogos)
│   └── settings.json                     # Configurações gerais e métricas predefinidas do sistema
│
├── docs/                                 # Documentação técnica do projeto
│   └── diagrama_classes_uml.md           # Diagrama de classes em Mermaid.js
│
├── src/                                  # Código-fonte principal da aplicação
│   ├── __init__.py                       
│   │
│   ├── models/                           # Entidades de domínio (classes do sistema)
│   │   ├── __init__.py                   
│   │   ├── categorias.py                 # Subclasses JogoCampanha, JogoCooperativo e JogoCompetitivo
│   │   ├── colecao.py                    # Classe Colecao (agregação de Jogo)
│   │   ├── jogo.py                       # Classe base Jogo
│   │   └── usuario.py                    # Classe Usuario (agregação de Colecao)
│   │
│   ├── repositories/                     # Camada de desacoplamento e persistência de dados
│   │   ├── __init__.py                   
│   │   └── persistencia.py               # Módulo único para gravação e leitura do arquivo JSON
│   │
│   └── services/                         # Regras de negócio e casos de uso do sistema
│       ├── __init__.py                   
│       ├── categorias_service.py         # Regras para categorias específicas de jogos
│       ├── colecao_service.py            # Gerenciamento de coleções
│       ├── jogo_service.py               # Cadastro e manipulação básica de jogos
│       ├── relatorio_service.py          # Cálculo de estatísticas e métricas do catálogo
│       └── usuario_service.py            # Operações de usuário
│
├── tests/                                # Testes automatizados com pytest
│   ├── __init__.py
│   ├── test_categorias.py                # Testes unitários para as subclasses de Jogo
│   ├── test_colecao.py                   # Testes unitários para a classe Colecao
│   ├── test_jogo.py                      # Testes unitários para a classe base Jogo
│   ├── test_persistencia.py              # Testes de leitura e salvamento no JSON
│   ├── test_regras_de_negocio.py         # Testes de integração das regras de negócio
│   └── test_usuario.py                   # Testes unitários para a classe Usuario
│
├── main.py                               # Ponto de entrada CLI (menu interativo do sistema)
├── README.md                             # Documentação principal e instruções de execução
└── requirements.txt                      # Dependências externas do projeto Python
```