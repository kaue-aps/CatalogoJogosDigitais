"""
Ponto de Entrada (CLI) do Sistema de Catálogo de Jogos Digitais
"""

import src.services.jogos_service as servico_jogo
import src.services.configuracao_service as servico_configuracao
import src.services.colecao_service as servico_colecao
import src.services.usuario_service as servico_usuario

from src.models.jogo import Jogo
from src.models.categorias import *


def menu_principal():
    print("\n" + "=" * 40)
    print("      CATÁLOGO DE JOGOS DIGITAIS")
    print("=" * 40)
    print("1. Gerenciar Meus Jogos")
    print("2. Gerenciar Minhas Coleções")
    print("3. Relatórios e Estatísticas")
    print("4. Configurações do Sistema")
    print("0. Sair")
    print("=" * 40)


# ==========================================
# SUBMENUS DE FLUXO
# ==========================================

def sub_menu_jogos():
    while True:
        print("\n--- GERENCIAR JOGOS ---")
        print("1. Cadastrar novo jogo")
        print("2. Listar todos os jogos")
        print("3. Buscar/Filtrar jogos (Título, Gênero, Status, Plataforma)")
        print("4. Busca ordenada de jogos (Avaliação ou Horas)")
        print("5. Atualizar progresso / Editar jogo")
        print("6. Avaliar jogo")
        print("7. Deletar jogo")
        print("0. Voltar ao menu principal")
        
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            print("\n\n[Desejarias cadastrar um jogo de qual categoria?]")
            print("1. Jogo genérico")
            print("2. Jogo campanha")
            print("3. Jogo competitivo")
            print("4. Jogo cooperativo")
            print("0. Voltar")

            sub_opcao = str(input("\nEscolha uma categoria: ")).strip()

            print("\n\n[Informe os dados do jogo]")
            titulo = str(input("Título: "))
            genero = str(input("\nGênero: "))
            plataforma = str(input("\nPlataforma: "))

            if sub_opcao == "1":
                jogo = Jogo(titulo, genero, plataforma)
            elif sub_opcao == "2":
                cap_totais = int(input("\nQuantidade de capítulos totais: "))
                jogo = JogoCampanha(titulo, genero, plataforma, cap_totais)
            elif sub_opcao == "3":
                jogo = JogoCompetitivo(titulo, genero, plataforma)
            elif sub_opcao == "4":
                max_jogadores = int((input("\nMáximo de jogadores suportados por sessão: ")))
                jogo = JogoCooperativo(titulo, genero, plataforma, max_jogadores)
            elif sub_opcao == "0":
                continue
            else:
                print("Escolha inválida!")
                continue

            servico_jogo.cadastrar_jogo(jogo)
            print(f"\n{jogo.titulo} CADASTRADO COM SUCESSO!")

        elif opcao == "2":
            lista_jogos = servico_jogo.listar_jogos()
            for jogo in lista_jogos:
                print(jogo)  # Aproveita o __str__ da classe de domínio

        elif opcao == "3":
            print("\n\n[Selecione o parâmetro de busca]")
            print("1. Buscar por parte do título")
            print("2. Buscar por gênero")
            print("3. Buscar por status")
            print("4. Buscar por plataforma")
            print("0. Voltar")

            sub_opcao = str(input("Escolha uma opção: ")).strip()

            if sub_opcao == "1":
                termo = str(input("Termo do título: "))
                lista_jogos = servico_jogo.buscar_por_titulo(termo)
            elif sub_opcao == "2":
                genero = str(input("Gênero do jogo: "))
                lista_jogos = servico_jogo.listar_por_genero(genero)
            elif sub_opcao == "3":
                status = str(input("Status do jogo: "))
                lista_jogos = servico_jogo.listar_por_status(status)
            elif sub_opcao == "4":
                plataforma = str(input("Plataforma do jogo: "))
                lista_jogos = servico_jogo.listar_por_plataforma(plataforma)
            elif sub_opcao == "0":
                continue
            else:
                print("Escolha inválida!")
                continue

            print(f"[{len(lista_jogos)} ENCONTRADOS]")
            for jogo in lista_jogos:
                print(jogo) # Aproveita o __str__ da classe de domínio

        elif opcao == "4":
            print("\n\n[Critério de ordenação]")
            print("1. Avaliação (Decrescente)")
            print("2. Avaliação (Crescente)")
            print("3. Horas jogadas (Decrescente)")
            print("4. Horas jogadas (Decrescente)")
            print("0. Voltar")

            sub_opcao = str(input("Escolha uma opção: ")).strip()

            if sub_opcao == "1":
                lista_jogos = servico_jogo.ordenar_jogos_por_avaliacao()
            elif sub_opcao == "2":
                lista_jogos = servico_jogo.ordenar_jogos_por_avaliacao(reverse=False)
            elif sub_opcao == "3":
                lista_jogos = servico_jogo.ordenar_jogos_por_horas_jogadas()
            elif sub_opcao == "4":
                lista_jogos = servico_jogo.ordenar_jogos_por_horas_jogadas(reverse=False)
            elif sub_opcao == "0":
                continue
            else:
                print("Escolha inválida")
                continue

            for jogo in lista_jogos:
                print(jogo)

        elif opcao == "5":
            pass
        elif opcao == "6":
            pass
        elif opcao == "7":
            pass
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")


def sub_menu_colecoes():
    while True:
        print("\n--- MINHAS COLEÇÕES ---")
        print("1. Criar nova coleção (ex: Favoritos, Zerados 2026)")
        print("2. Listar minhas coleções")
        print("3. Ver jogos de uma coleção")
        print("4. Adicionar jogo a uma coleção")
        print("5. Remover jogo de uma coleção")
        print("6. Deletar coleção")
        print("0. Voltar ao menu principal")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            pass
        elif opcao == "2":
            pass
        elif opcao == "3":
            pass
        elif opcao == "4":
            pass
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")


def sub_menu_relatorios():
    while True:
        print("\n--- RELATÓRIOS E ESTATÍSTICAS ---")
        print("1. Total de horas jogadas")
        print("2. Top 5 jogos mais jogados")
        print("3. Percentual de jogos por Status (Jogando, Finalizado, Não Iniciado)")
        print("4. Média de avaliação dos jogos finalizados")
        print("0. Voltar ao menu principal")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            pass
        elif opcao == "2":
            pass
        elif opcao == "3":
            pass
        elif opcao == "4":
            pass
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")


def sub_menu_configuracoes():
    while True:
        print("\n--- CONFIGURAÇÕES DO SISTEMA ---")
        print("1. Ver configurações atuais")
        print("2. Alterar meta anual de jogos finalizados")
        print("3. Alterar plataforma principal / gêneros favoritos")
        print("0. Voltar ao menu principal")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            pass
        elif opcao == "2":
            pass
        elif opcao == "3":
            pass
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")


# ==========================================
# FLUXO PRINCIPAL DE EXECUÇÃO
# ==========================================

def main():
    while True:
        menu_principal()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            sub_menu_jogos()
        elif opcao == "2":
            sub_menu_colecoes()
        elif opcao == "3":
            sub_menu_relatorios()
        elif opcao == "4":
            sub_menu_configuracoes()
        elif opcao == "0":
            print("\nEncerrando o sistema... Até logo!")
            break
        else:
            print("\nOpção inválida! Tente novamente.")


if __name__ == "__main__":
    main()