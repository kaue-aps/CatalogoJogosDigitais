## 🏗️ Estrutura de Classes (Diagrama UML)

Com o intuito de não poluir a representação visual, decidi omitir os **métodos especiais** e os **atributos derivados** (obtidos via *getters*). Também optei por não representar as duas classes de repositório (CatalogoJSON e ConfiguracaoJSON), uma vez que elas têm estruturas simples e não estão relacionadas ao problema

```mermaid
classDiagram
    class Jogo {
        -str titulo
        -str genero
        -str plataforma
        -str status
        -float horas_jogadas
        -float avaliacao
        -date data_inicio
        -date data_termino
        -int id
        +registrar_progresso()
        +finalizar_jogo()
        +reiniciar_jogo()
        +avaliar_jogo()
    }

    class JogoCampanha {
        -int capitulos_totais
        -int capitulos_concluidos
        -float percentual_conclusao
        +avancar_capitulo()
    }

    class JogoCompetitivo {
        -int partidas_jogadas
        -int vitorias
        -int derrotas
        -str ranking_atual
        +registrar_partida()
        +atualizar_ranking()
    }

    class JogoCooperativo {
        -int max_jogadores
        -int sessoes_coop
        -list~str~ participantes_frequentes
        +adicionar_participante()
        +registrar_sessao()
    }

    class Colecao {
        -str nome
        -list~Jogo~ jogos
        -int id
        +adicionar_jogo()
        +remover_jogo()
        +listar_jogos()
    }

    class Usuario {
        -str nome
        -list~Colecao~ colecoes
        -int id
        +adicionar_colecao()
        +listar_colecoes()
        +remover_colecao()
    }

    Jogo <|-- JogoCampanha
    Jogo <|-- JogoCompetitivo
    Jogo <|-- JogoCooperativo
    Colecao "0..*" o-- "0..*" Jogo : agrupa
    Usuario "0..*" o-- "0..*" Colecao : possui
```
