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
