"""Módulo com a interface de comandos CLI"""

import argparse

def criar_parser():
    # Parser Principal
    parser = argparse.ArgumentParser(description="Sistema de Gerenciamento do Catálogo Pessoal de Jogos Digitais")
    subparsers_principais = parser.add_subparsers(dest="modulo", help="Módulo de atuação")

    # =========================================================================
    # 1. MÓDULO: JOGOS (python main.py jogos ...)
    # =========================================================================
    parser_jogos = subparsers_principais.add_parser("jogos", help="Gerenciamento do catálogo de jogos")
    subparsers_jogos = parser_jogos.add_subparsers(dest="acao", help="Ação a ser executada em jogos")

    # --- jogos cadastrar ---
    # 1. Campos Genéricos / Obrigatórios
    p_cadastrar = subparsers_jogos.add_parser("cadastrar", help="Cadastra um novo jogo no catálogo")
    p_cadastrar.add_argument("--titulo", required=True, type=str, help="Título do jogo")
    p_cadastrar.add_argument("--genero", required=True, type=str, help="Gênero do jogo")
    p_cadastrar.add_argument("--plataforma", required=True, type=str, help="Plataforma (PC, Console, Mobile)")

    p_cadastrar.add_argument(
        "--tipo", 
        choices=["generico", "campanha", "competitivo", "cooperativo"], 
        default="generico", 
        help="Tipo de experiência de jogo (categoria)"
    )

    # 2. Campos Específicos para JogoCampanha
    p_cadastrar.add_argument("--capitulos-totais", type=int, default=1, help="Total de capítulos/missões (Campanha)")

    # 3. Campos Específicos para JogoCooperativo
    p_cadastrar.add_argument("--max-jogadores", type=int, default=2, help="Número máximo de jogadores por sessão (Cooperativo)")

    # --- jogos listar ---
    p_listar = subparsers_jogos.add_parser("listar", help="Lista todos os jogos do catálogo")

    # --- jogos buscar ---
    p_buscar = subparsers_jogos.add_parser("buscar", help="Busca/Filtra jogos por atributos")
    p_buscar.add_argument("--titulo", type=str, help="Buscar por parte do título")
    p_buscar.add_argument("--genero", type=str, help="Filtrar por gênero")
    p_buscar.add_argument("--status", type=str, help="Filtrar por status (NÃO INICIADO, JOGANDO, FINALIZADO)")
    p_buscar.add_argument("--plataforma", type=str, help="Filtrar por plataforma")

    # --- jogos ordenar ---
    p_ordenar = subparsers_jogos.add_parser("ordenar", help="Exibe os jogos do catálogo de forma ordenada")
    p_ordenar.add_argument("--por", choices=["avaliacao", "horas"], required=True, help="Atributo para ordenação")
    p_ordenar.add_argument("--crescente", action="store_true", help="Se informado, ordena de forma crescente (padrão: decrescente)")

    # --- jogos avaliar ---
    p_avaliar = subparsers_jogos.add_parser("avaliar", help="Atribui uma nota ao jogo depois de finalizado")
    p_avaliar.add_argument("--id", required=True, type=int, help="ID do jogo")
    p_avaliar.add_argument("--nota", required=True, type=float, help="Nota do jogo (0.0 a 10.0)")

    # --- jogos deletar ---
    p_deletar = subparsers_jogos.add_parser("deletar", help="Remove um jogo do catálogo")
    p_deletar.add_argument("--id", required=True, type=int, help="ID do jogo a ser removido")

    # =========================================================================
    # 2. MÓDULO: COLEÇÕES (python main.py colecoes ...)
    # =========================================================================
    parser_colecoes = subparsers_principais.add_parser("colecoes", help="Gerenciamento de coleções personalizadas")
    subparsers_colecoes = parser_colecoes.add_subparsers(dest="acao", help="Ação em coleções")

    # --- colecoes criar ---
    p_col_criar = subparsers_colecoes.add_parser("criar", help="Cria uma nova coleção personalizada")
    p_col_criar.add_argument("--nome", required=True, type=str, help="Nome da coleção (ex: Favoritos)")

    # --- colecoes listar ---
    p_col_listar = subparsers_colecoes.add_parser("listar", help="Listar todas as coleções do sistema")

    # --- colecoes ver ---
    p_col_ver = subparsers_colecoes.add_parser("ver", help="Exibe os jogos dentro de uma coleção específica")
    p_col_ver.add_argument("--nome", required=True, type=str, help="Nome da coleção")

    # --- colecoes adicionar-jogo ---
    p_col_add = subparsers_colecoes.add_parser("adicionar-jogo", help="Adiciona um jogo a uma coleção")
    p_col_add.add_argument("--id-jogo", required=True, type=int, help="ID do jogo a adicionar")
    p_col_add.add_argument("--id-colecao", required=True, type=int, help="ID da coleção")

    # --- colecoes remover-jogo ---
    p_col_rem = subparsers_colecoes.add_parser("remover-jogo", help="Remove um jogo de uma coleção")
    p_col_rem.add_argument("--id-jogo", required=True, type=int, help="ID do jogo a remover")
    p_col_rem.add_argument("--id-colecao", required=True, type=int, help="ID da coleção")

    # --- colecoes deletar ---
    p_col_del = subparsers_colecoes.add_parser("deletar", help="Apaga uma coleção existente")
    p_col_del.add_argument("--id", required=True, type=int, help="ID da coleção a apagar")

    # =========================================================================
    # 3. MÓDULO: RELATÓRIOS (python main.py relatorio ...)
    # =========================================================================
    parser_relatorio = subparsers_principais.add_parser("relatorio", help="Geração de estatísticas e relatórios do catálogo")
    parser_relatorio.add_argument(
        "--tipo",
        choices=["total-jogos", "total-horas", "top5-mais-jogados", "percentual-por-status", "media-avaliacao"],
        required=True,
        help="Tipo de relatório a ser exibido"
    )


    # =========================================================================
    # 4. MÓDULO: CONFIGURAÇÕES (python main.py config ...)
    # =========================================================================
    parser_config = subparsers_principais.add_parser("config", help="Configurações do sistema (settings.json)")
    subparsers_config = parser_config.add_subparsers(dest="acao", help="Ação de configuração")

    # --- config ver ---
    subparsers_config.add_parser("exibir", help="Exibe as configurações atuais do sistema")

    # --- config redefinir ---
    p_cfg_up = subparsers_config.add_parser("redefinir", help="Redefine configurações do sistema ou preferências do usuário")
    p_cfg_up.add_argument("--meta-anual", type=int, help="Nova meta de jogos finalizados por ano")
    p_cfg_up.add_argument("--plataforma-principal", choices=["PC", "Console", "Mobile"], type=str, help="Definir plataforma principal")
    p_cfg_up.add_argument("--limite-andamento", type=int, help="Novo limite de jogos em andamento (com status 'JOGANDO')")
    p_cfg_up.add_argument("--generos-favoritos", nargs="+", type=str, help="Definir até 3 gêneros favoritos (separados por espaços)")


    # =========================================================================
    # 5. MÓDULO: USUÁRIOS (python main.py usuarios ...)
    # =========================================================================

    parser_usuarios = subparsers_principais.add_parser("usuarios", help="Gerenciamento de usuários do sistema")
    subparsers_usuarios = parser_usuarios.add_subparsers(dest="acao", help="Ação de configuração")

    # --- usuarios cadastrar ---
    p_user_cadastrar = subparsers_usuarios.add_parser("cadastrar", help="Cadastra um novo usuário no sistema")
    p_user_cadastrar.add_argument("--nome", required=True, type="str", help="Nome ou nickname do usuário")

    # --- usuarios deletar ---
    p_user_deletar = subparsers_usuarios.add_parser("deletar", help="Exclui um usuário existente do sistema")
    p_user_deletar.add_argument("--id", required=True, type="int", help="ID do usuário cadastrado")

    # --- usuarios adicionar-colecao ---
    p_user_add = subparsers_usuarios.add_parser("adicionar-colecao", help="Adiciona uma coleção existente à lista de coleções do usuário")
    p_user_add.add_argument("--id-colecao", required=True, type="int", help="ID da coleção")
    p_user_add.add_argument("--id-usuario", required=True, type="int", help="ID do usuario")

    # --- usuarios remover-colecao ---
    p_user_remove = subparsers_usuarios.add_parser("remover-colecao", help="Remove uma coleção existente da lista de coleções do usuário")
    p_user_remove.add_argument("--id-colecao", required=True, type="int", help="ID da coleção")
    p_user_remove.add_argument("--id-usuario", required=True, type="int", help="ID do usuario")

    # --- usuarios listar ---
    subparsers_usuarios.add_parser("listar", help="Lista todos os usuários do sistema")

    # --- usuarios listar-colecoes ---
    p_user_col = subparsers_usuarios.add_parser("listar-colecoes", help="Lista todas as coleções do usuário informado")
    p_user_col.add_argument("--id", required=True, type=int, help="ID do usuário")

    # --- usuarios resumo ---
    p_user_see = subparsers_usuarios.add_parser("resumo", help="Exibe a quantidade de coleções e de jogos do usuário")
    p_user_see.add_argument("--id", required=True, type="int", help="ID do usuário")


    return parser