"""
Ponto de Entrada (CLI) do Catálogo de Jogos Digitais via subcomandos. Orquestra apenas o fluxo de execução

Exemplo de uso:
  python main.py jogos cadastrar --titulo "Hades" --genero "Rogue-like" --plataforma "PC" --tipo campanha
  python main.py jogos buscar --genero "RPG"
  python main.py colecoes adicionar --nome "Favoritos" --id-jogo 1
  python main.py relatorio --tipo top5
"""

from cli import criar_parser

import src.services.jogos_service as servico_jogos
import src.services.colecao_service as servico_colecoes
import src.services.relatorio_service as servico_relatorios
import src.services.configuracao_service as servico_configuracoes
import src.services.usuario_service as servico_usuarios

from src.models.jogo import Jogo
from src.models.categorias import *
from src.models.colecao import Colecao
from src.models.usuario import Usuario


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
            print(servico_configuracoes.configuracoes_atuais())
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

    # === MÓDULO USUÁRIOS ===
    elif args.modulo == "usuarios":

        if args.acao == "cadastrar":
            usuario = Usuario(args.nome)
            try:
                servico_usuarios.cadastrar_usuario(usuario)
                print(f"Usuário cadastrado com sucesso!")
            except Exception as e:
                print(f"Erro ao cadastrar usuário: {e}")

        elif args.acao == "deletar":
            try:
                servico_usuarios.deletar_usuario(args.id)
                print("Usuário deletado com sucesso!")
            except Exception as e:
                print(f"Erro ao deletar usuário: {e}")

        elif args.acao == "adicionar-colecao":
            try:
                servico_usuarios.adicionar_colecao_ao_usuario(args.id_colecao, args.id_usuario)
                print(f"Coleção adicionada à lista do usuário com sucesso!")
            except Exception as e:
                print(f"Erro ao adicionar coleção à lista do usuário: {e}")

        elif args.acao == "remover-colecao":
            try:
                servico_usuarios.remover_colecao_do_usuario(args.id_colecao, args.id_usuario)
                print(f"Coleção removida da lista do usuário com sucesso!")
            except Exception as e:
                print(f"Erro ao remover coleção da lista do usuário: {e}")

        elif args.acao == "listar":
            print(servico_usuarios.listar_usuarios())

        elif args.acao == "listar-colecoes":
            try:
                print(servico_usuarios.listar_colecoes(args.id_usuario))
            except Exception as e:
                print(f"Erro ao listar coleções do usuário: {e}")

        elif args.acao == "resumo":
            try:
                print(servico_usuarios.get_by_id(args.id_usuario))
            except Exception as e:
                print(f"Erro ao exibir resumo do usuário: {e}")


if __name__ == "__main__":
    main()