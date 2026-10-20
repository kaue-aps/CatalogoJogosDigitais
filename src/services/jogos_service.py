"""
Serviços de Jogos

Contém funções específicas para jogos genéricos ou de categoria

Responsabilidades:
- Orquestrar o CRUD básico de jogos
- Garantir regras de negócio ao manipular esses jogos
"""

from src.repositories.persistencia import CatalogoJSON
from src.models.jogo import Jogo
from src.models.categorias import *

catalogo = CatalogoJSON("data/catalogo.json")

def proximo_id_jogos():
    dados = catalogo.carregar()
    maior = 0 # Começa em 0 para que o retorno mínimo (maior + 1) seja 1

    for categoria in dados["jogos"].values():
        # Só vamos olhar para categorias que têm jogos
        if categoria:
            maximo_da_categoria = max(jogo["id"] for jogo in categoria)
            if maximo_da_categoria > maior:
                maior = maximo_da_categoria

    return maior + 1


def cadastrar_jogo_generico(jogo: Jogo):
    dados = catalogo.carregar()
    for jogo_cadastrado in dados["jogos"]["genericos"]:
        # Faz a comparação com base nos parâmetros do método __eq__ definido na classe de domínio
        if jogo == Jogo.from_dict(jogo_cadastrado):
            raise PermissionError("O jogo informado já está cadastrado na base de dados")
    jogo.id = proximo_id_jogos()
    dados["jogos"]["genericos"].append(jogo.to_dict())
    catalogo.salvar(dados)




def deletar_jogo(id: int):
    dados = catalogo.carregar()
    for categoria in dados["jogos"].values():
        for jogo in categoria:
            if jogo["id"] == id:
                categoria.remove(jogo)
                catalogo.salvar(dados)
                return
    raise ValueError("ID do jogo não encontrado.")


def get_by_id(id: int):
    dados = catalogo.carregar()
    for categoria in dados["jogos"].values():
        for jogo in categoria:
            if jogo["id"] == id:
                return Jogo.from_dict(jogo)