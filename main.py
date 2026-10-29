"""
Ponto de Entrada (CLI) do Catálogo de Jogos Digitais via Subcomandos
Exemplo de uso:
  python main.py jogos cadastrar --titulo "Hades" --genero "Rogue-like" --plataforma "PC" --tipo campanha
  python main.py jogos buscar --genero "RPG"
  python main.py colecoes adicionar --nome "Favoritos" --id-jogo 1
  python main.py relatorio --tipo top5
"""

import argparse

import src.services.jogos_service as servico_jogos
import src.services.colecao_service as servico_colecoes
import src.services.relatorio_service as servico_relatorios
import src.services.configuracao_service as servico_configuracoes

from src.models.jogo import Jogo
from src.models.categorias import *
from src.models.colecao import Colecao


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

    # AINDA VOU VER ISSO AQUI
    # --- jogos atualizar ---
    # p_atualizar = subparsers_jogos.add_parser("atualizar", help="Atualiza informações de um jogo existente")
    # p_atualizar.add_argument("--horas", type=float, help="Horas jogadas a adicionar ou definir")
    # p_atualizar.add_argument("--status", type=str, help="Novo status do jogo")

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
    p_col_listar = subparsers_colecoes.add_parser("listar", help="Listar todas as coleções do usuário")

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

    return parser

def main():
    parser = criar_parser()
    args = parser.parse_args()

    # Se o usuário apenas rodar "python main.py" sem informar nenhum comando
    if not args.modulo:
        parser.print_help()
        return

    # =========================================================================
    # EXECUÇÃO DAS AÇÕES (ROUTING)
    # =========================================================================

    # === MÓDULO JOGOS ===
    if args.modulo == "jogos":
        if args.acao == "cadastrar":
            # Exemplo de como instanciar a subclasse correta com base no --tipo
            if args.tipo == "generico":
                jogo = Jogo(args.titulo, args.genero, args.plataforma)
            elif args.tipo == "campanha":
                jogo = JogoCampanha(args.titulo, args.genero, args.plataforma, args.capitulos_totais)
            elif args.tipo == "competitivo":
                jogo = JogoCompetitivo(args.titulo, args.genero, args.plataforma)
            elif args.tipo == "cooperativo":
                jogo = JogoCooperativo(args.titulo, args.genero, args.plataforma, args.max_jogadores)

            try:
                servico_jogos.cadastrar_jogo(jogo)
                print(f"Jogo '{args.titulo}' cadastrado com sucesso!")
            except Exception as e:
                print(f"Erro ao cadastrar jogo: {e}")
            
        elif args.acao == "listar":
            jogos = servico_jogos.listar_jogos()
            for j in jogos:
                print(j) # Imprime de acordo com a string definida em __str__

        elif args.acao == "buscar":
            if args.titulo:
                res = servico_jogos.buscar_por_titulo(args.titulo)
            elif args.genero:
                res = servico_jogos.listar_por_genero(args.genero)
            elif args.status:
                res = servico_jogos.listar_por_status(args.status)
            elif args.plataforma:
                res = servico_jogos.listar_por_plataforma(args.plataforma)
            else:
                res = []
            
            for j in res:
                print(j)

        elif args.acao == "ordenar":
            is_reverse = not args.crescente # Se passou --crescente, reverse fica False
            if args.por == "avaliacao":
                res = servico_jogos.ordenar_jogos_por_avaliacao(reverse=is_reverse)
            else:
                res = servico_jogos.ordenar_jogos_por_horas_jogadas(reverse=is_reverse)

            for j in res:
                print(j)

        # elif args.acao == "atualizar":
        #     dados = {}
        #     if args.horas is not None:
        #         dados["horas_jogadas"] = args.horas
        #     if args.status:
        #         dados["status"] = args.status
        #     servico_jogos.atualizar_jogo(args.id, dados)
        #     print(f"Jogo {args.id} atualizado com sucesso!")

        elif args.acao == "avaliar":
            try:
                servico_jogos.avaliar_jogo(args.id, args.nota)
                print(f"Jogo {args.id} avaliado com nota {args.nota}!")
            except Exception as e:
                print(f"Erro ao avaliar: {e}")

        elif args.acao == "deletar":
            try:
                servico_jogos.deletar_jogo(args.id)
                print(f"Jogo {args.id} deletado com sucesso!")
            except Exception as e:
                print(f"Erro: {e}")

    # === MÓDULO COLEÇÕES ===
    elif args.modulo == "colecoes":
        if args.acao == "criar":
            colecao = Colecao(args.nome)
            try:
                servico_colecoes.cadastrar_colecao(colecao)
                print(f"Coleção '{args.nome}' criada!")
            except Exception as e:
                print(f"Erro ao criar coleção: {e}")

        elif args.acao == "adicionar_jogo":
            try:
                servico_colecoes.adicionar_jogo_a_colecao(args.id_jogo, args.id_colecao)
                print(f"Jogo adicionado à coleção!")
            except Exception as e:
                print(f"Erro ao adicionar jogo à coleção: {e}")

        elif args.acao == "remover_jogo":
            try:
                servico_colecoes.remover_jogo_da_colecao(args.id_jogo, args.id_colecao)
                print(f"Jogo removido da coleção!")
            except Exception as e:
                print(f"Erro ao adicionar jogo à coleção: {e}")

        elif args.acao == "deletar":
            try:
                servico_colecoes.deletar_colecao(args.id)
                print("Coleção apagada com sucesso!")
            except Exception as e:
                print(f"Erro ao deletar coleção: {e}")

    # === MÓDULO RELATÓRIO ===
    elif args.modulo == "relatorio":
        if args.tipo == "total-jogos":
            total = servico_relatorios.total_de_jogos_cadastrados()
            print(f"O Catálogo possui um total de {total} jogos cadastrados")
        
        elif args.tipo == "total-horas":
            total = servico_relatorios.total_de_horas_jogadas()
            print(f"Você possui um total de {total} horas jogadas")

        elif args.tipo == "media-avaliacao":
            media = servico_relatorios.media_de_avaliacao_jogos()
            print(f"A média de avaliação dos jogos é {media}")

        elif args.tipo == "percentual-por-status":
            valores = servico_relatorios.percentual_de_jogos_por_status() # retorna um dicionário
            print(f"NÃO INICIADOS: {valores["NAO INICIADO"]}%\n"
                  f"JOGANDO: {valores["JOGANDO"]}%\n"
                  f"FINALIZADOS: {valores["FINALIZADO"]}%")

        elif args.tipo == "top5-mais-jogados":
            top5 = servico_relatorios.top_5_jogos_mais_jogados()
            print(f"1º - {top5["1º"].titulo} - {top5["1º"].horas_jogadas}h")
            print(f"2º - {top5["2º"].titulo} - {top5["2º"].horas_jogadas}h")
            print(f"3º - {top5["3º"].titulo} - {top5["3º"].horas_jogadas}h")
            print(f"4º - {top5["4º"].titulo} - {top5["4º"].horas_jogadas}h")
            print(f"5º - {top5["5º"].titulo} - {top5["5º"].horas_jogadas}h")

    # === MÓDULO CONFIGURAÇÕES ===
    elif args.modulo == "config":
        if args.acao == "exibir":
            # servico_configuracoes.exibir()
            pass
        elif args.acao == "redefinir":
            if args.meta_anual:
                try:
                    servico_configuracoes.redefinir_meta_anual(args.meta_anual)
                    print(f"Meta anual redefinida para {args.meta_anual} jogos")
                except Exception as e:
                    print(f"Erro ao redefinir meta anual de jogos finalizados: {e}")

            if args.plataforma_principal:
                try:
                    servico_configuracoes.redefinir_plataforma_principal(args.plataforma_principal)
                    print(f"Plataforma principal redefinida para {args.plataforma_principal}")
                except Exception as e:
                    print(f"Erro ao redefinir plataforma principal: {e}")

            if args.limite_andamento:
                try:
                    servico_configuracoes.redefinir_limite_jogos_andamento(args.limite_andamento)
                    print(f"Limite de jogos em andamento redefinido para {args.limite_andamento}")
                except Exception as e:
                    print(f"Erro ao redefinir limite de jogos em andamento: {e}")

            if args.generos_favoritos:
                try:
                    servico_configuracoes.redefinir_generos_favoritos(args.generos_favoritos)
                    print(f"Gêneros favoritos redefinidos com sucesso!")
                except Exception as e:
                    print(f"Erro ao redefinir gêneros favoritos: {e}")


if __name__ == "__main__":
    main()