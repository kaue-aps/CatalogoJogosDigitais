# Guia de subcomandos da CLI

Os comandos abaixo são executados a partir da pasta raiz do projeto com `python main.py`. Argumentos entre `< >` são valores a informar; opções entre `[ ]` são opcionais. Quando indicado, os valores entre chaves representam as escolhas aceitas pelo parser.

```text
main.py
├── jogos
│   ├── cadastrar --titulo <str> --genero <str> --plataforma <str>
│   │              [--tipo {generico,campanha,competitivo,cooperativo}]
│   │              [--capitulos-totais <int>] [--max-jogadores <int>]
│   ├── listar
│   ├── buscar [--titulo <str>] [--genero <str>] [--status <str>] [--plataforma <str>]
│   ├── ordenar --por {avaliacao,horas} [--crescente]
│   ├── avaliar --id <int> --nota <float>
│   ├── deletar --id <int>
│   └── registrar-progresso --id <int> --horas <float>
│
├── jogos-campanha
│   ├── avancar-capitulo --id <int> [--capitulos <int>]
│   └── percentual_conclusao --id <int>
│
├── jogos-competitivo
│   ├── atualizar-ranking --id <int> --novo_ranking <str>
│   ├── registrar-partida --id <int> --resultado <str>
│   └── taxa-vitoria --id <int>
│
├── jogos-cooperativo
│   ├── adicionar-participante --id <int> --nome <str>
│   └── registrar-sessao --id <int>
│
├── colecoes
│   ├── criar --nome <str>
│   ├── listar
│   ├── ver --nome <str>
│   ├── adicionar-jogo --id-jogo <int> --id-colecao <int>
│   ├── remover-jogo --id-jogo <int> --id-colecao <int>
│   └── deletar --id <int>
│
├── relatorio --tipo {total-jogos,total-horas,top5-mais-jogados,
│                     percentual-por-status,media-avaliacao}
│
├── config
│   ├── exibir
│   └── redefinir [--meta-anual <int>] [--plataforma-principal {PC,Console,Mobile}]
│                 [--limite-andamento <int>] [--generos-favoritos <str>...]
│
└── usuarios
    ├── cadastrar --nome <str>
    ├── deletar --id <int>
    ├── adicionar-colecao --id-colecao <int> --id-usuario <int>
    ├── remover-colecao --id-colecao <int> --id-usuario <int>
    ├── listar
    ├── listar-colecoes --id <int>
    └── resumo --id <int>
```

## Valores padrão e observações

- Em `jogos cadastrar`, `--tipo` usa `generico` por padrão, `--capitulos-totais` usa `1` e `--max-jogadores` usa `2`.
- Em `jogos-campanha avancar-capitulo`, `--capitulos` usa `1`.
- `jogos buscar` aceita os filtros como opcionais; o parser não exige que um deles seja informado.
- `jogos ordenar` exige `--por`. A ordenação é decrescente por padrão; `--crescente` altera a direção.
- `config redefinir` aceita qualquer combinação das opções apresentadas. `--generos-favoritos` recebe um ou mais gêneros.
- `relatorio` é um módulo com a opção obrigatória `--tipo`, não possui subcomandos adicionais.
