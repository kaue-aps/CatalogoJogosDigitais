"""
Serviços de Coleção

Responsabilidades:
- Orquestrar o CRUD básico de coleções no catálogo
- Garantir regras de negócio
"""

from src.repositories.persistencia import CatalogoJSON
from src.models.colecao import Colecao
import src.services.jogos_service as servico_jogo

catalogo = CatalogoJSON("data/catalogo.json")

def proximo_id_colecao():
    dados = catalogo.carregar()
    maior = 0 # Começa em 0 para que o retorno mínimo (maior + 1) seja 1

    # Se houver alguma coleção cadastrada
    if dados["colecoes"]:
        id_maximo = max(colecao["id"] for colecao in dados["colecoes"])
        if id_maximo > maior:
            maior = id_maximo

    return maior + 1


def cadastrar_colecao(colecao: Colecao):
    dados = catalogo.carregar()
    for colecao_cadastrada in dados["colecoes"]:
        # Faz a comparação com base nos parâmetros do método __eq__ definido na classe de domínio
        if colecao == Colecao.from_dict(colecao_cadastrada):
            raise PermissionError("A coleção informada já está cadastrado no sistema")
    colecao._id = proximo_id_colecao()
    dados["colecao"].append(colecao.to_dict())
    catalogo.salvar(dados)


def deletar_colecao(id: int):
    dados = catalogo.carregar()
    for colecao in dados["colecoes"]:
        if colecao["id"] == id:
            dados["colecoes"].remove(colecao)
            catalogo.salvar(dados)
            return 
    raise ValueError("ID da coleção não encontrado.")


def get_by_id(id: int):
    dados = catalogo.carregar()
    for colecao in dados["colecoes"]:
        if colecao["id"] == id:
            return Colecao.from_dict(colecao)
    raise ValueError("ID da coleção não encontrado.")


def adicionar_jogo_a_colecao(id_do_jogo: int, id_da_colecao: int):
    dados = catalogo.carregar()
    jogo = servico_jogo.get_by_id(id_do_jogo)
    colecao = get_by_id(id_da_colecao)

    for colec in dados["colecoes"]:
        if colec["id"] == id_da_colecao:
            if id_do_jogo not in colec["id_jogos"]:
                colec["id_jogos"].append(id_do_jogo)
                catalogo.salvar[dados]
                colecao.adicionar_jogo(jogo)
                return colecao


def remover_jogo_da_colecao(id_do_jogo: int, id_da_colecao: int):
    dados = catalogo.carregar()
    for colecao in dados["colecoes"]:
        if colecao["id"] == id_da_colecao:
            if id_do_jogo in colecao["id_jogos"]:
                colecao["id_jogos"].remove(id_do_jogo)
                catalogo.salvar(dados)
                return

            