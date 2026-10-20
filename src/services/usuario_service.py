"""
Serviços de Usuario

Responsabilidades:
- 
- 
"""

from src.repositories.persistencia import CatalogoJSON
import src.services.colecao_service as servico_colecao
from src.models.usuario import Usuario

catalogo = CatalogoJSON("data/catalogo.json")

def proximo_id_usuario():
    dados = catalogo.carregar()
    maior = 0 # Começa em 0 para que o retorno mínimo (maior + 1) seja 1

    # Se houver algum usuário cadastrado
    if dados["usuarios"]:
        id_maximo = max(usuario["id"] for usuario in dados["usuarios"])
        if id_maximo > maior:
            maior = id_maximo

    return maior + 1


def cadastrar_usuario(usuario: Usuario):
    dados = catalogo.carregar()
    for usuario_cadastrado in dados["usuarios"]:
        # Faz a comparação com base nos parâmetros do método __eq__ definido na classe de domínio
        if usuario == Usuario.from_dict(usuario_cadastrado):
            raise PermissionError("O usuário informado já está cadastrado no sistema")
    usuario.id = proximo_id_usuario()
    dados["usuario"].append(usuario.to_dict())
    catalogo.salvar(dados)


def deletar_usuario(id: int):
    dados = catalogo.carregar()
    for usuario in dados["usuarios"]:
        if usuario["id"] == id:
            dados["usuarios"].remove(usuario)
            catalogo.salvar(dados)
            return 
    raise ValueError("ID do usuário não encontrado.")


def get_by_id(id: int):
    dados = catalogo.carregar()
    for usuario in dados["usuarios"]:
        if usuario["id"] == id:
            return Usuario.from_dict(usuario)
    raise ValueError("ID do usuário não encontrado.")


def adicionar_colecao_ao_usuario(id_da_colecao: int, id_do_usuario: int):
    dados = catalogo.carregar()
    colecao = servico_colecao.get_by_id(id_da_colecao)
    usuario = get_by_id(id_do_usuario)

    for user in dados["usuarios"]:
        if user["id"] == id_do_usuario:
            if id_da_colecao not in user["id_colecoes"]:
                user["id_colecoes"].append(id_da_colecao)
                catalogo.salvar[dados]
                usuario.adicionar_colecao(colecao)
                return usuario


def remover_colecao_do_usuario(id_da_colecao: int, id_do_usuario: int):
    dados = catalogo.carregar()
    for usuario in dados["usuarios"]:
        if usuario["id"] == id_do_usuario:
            if id_da_colecao in usuario["id_colecoes"]:
                usuario["id_colecoes"].remove(id_da_colecao)
                catalogo.salvar(dados)
                return

            