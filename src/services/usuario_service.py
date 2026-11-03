"""
Serviços de Usuario

Responsabilidades:
- Fazer o CRUD básico de usuários do sistema
- Gerenciar as coleções pertencentes a um usuário
"""

from src.repositories.persistencia import CatalogoJSON
from src.models.usuario import Usuario
from src.services.colecao_service import get_by_id

caminho = "data/catalogo.json"
catalogo = CatalogoJSON(caminho)

def proximo_id_usuario() -> int:
    """Retorna um ID único para o próximo usuário. É calculado com base no maior ID de usuário existente"""

    dados = catalogo.carregar()
    maior = 0 # Começa em 0 para que o retorno mínimo (maior + 1) seja 1

    # Se houver algum usuário cadastrado
    if dados["usuarios"]:
        id_maximo = max(usuario["id"] for usuario in dados["usuarios"])
        if id_maximo > maior:
            maior = id_maximo

    return maior + 1


def cadastrar_usuario(usuario: Usuario) -> None:
    """Cadastra um novo usuário no sistema
    
    Raises:
        PermissionError: caso o usuário informado já esteja cadastrado no sistema
    """

    dados = catalogo.carregar()
    for usuario_cadastrado in dados["usuarios"]:
        # Faz a comparação com base nos parâmetros do método __eq__ definido na classe de domínio
        if usuario == Usuario.from_dict(usuario_cadastrado):
            raise PermissionError("O usuário informado já está cadastrado no sistema")
    usuario._id = proximo_id_usuario()
    dados["usuarios"].append(usuario.to_dict())
    catalogo.salvar(dados)


def deletar_usuario(id: int) -> None:
    """Exclui o cadastro de um usuário do sistema
    
    Raises:
        ValueError: caso o usuário não seja encontrado pelo ID informado
    """

    dados = catalogo.carregar()
    for usuario in dados["usuarios"]:
        if usuario["id"] == id:
            dados["usuarios"].remove(usuario)
            catalogo.salvar(dados)
            return 
    raise ValueError("ID do usuário não encontrado.")


def listar_usuarios() -> str:
    """Retorna uma string vertical com o nome de todos os usuários cadastrados no sistema"""

    dados = catalogo.carregar()
    lista = "========== USUARIOS CADASTRADOS ==========\n"
    for usuario in dados["usuarios"]:
        lista += f"{usuario["nome"]}\n"

    return lista


def listar_colecoes(id_do_usuario) -> str:
    """Retorna uma string vertical com o nome de todas as coleções do usuário"""

    dados = catalogo.carregar()
    for usuario in dados["usuarios"]:
        if usuario["id"] == id_do_usuario:
            lista = f"========== COLEÇÕES DE {usuario["nome"]} ==========\n"
            for id_colecao in usuario["id_colecoes"]:
                lista += f"{get_by_id(id_colecao)._nome}\n"
            return lista
        
    raise ValueError("ID do usuário não encontrado")
    
            
def get_by_id(id: int):
    """Retorna um usuário instanciado a partir do ID
    
    Raises:
        ValueError: caso o usuário não seja encontrado pelo ID informado 
    """

    dados = catalogo.carregar()
    for usuario in dados["usuarios"]:
        if usuario["id"] == id:
            return Usuario.from_dict(usuario)
    raise ValueError("ID do usuário não encontrado.")

def adicionar_colecao_ao_usuario(id_da_colecao: int, id_do_usuario: int) -> None:
    """Adiciona uma coleção existente à lista de coleções do usuário
    
    Raises:
        ValueError: caso a coleção ou o usuário não sejam encontrados pelo ID
    """

    dados = catalogo.carregar()

    for user in dados["usuarios"]:
        if user["id"] == id_do_usuario:
            if id_da_colecao not in user["id_colecoes"]:
                user["id_colecoes"].append(id_da_colecao)
                catalogo.salvar[dados]
                return
    raise ValueError("ID da coleção ou ID do usuário não encontrados")


def remover_colecao_do_usuario(id_da_colecao: int, id_do_usuario: int) -> None:
    """Remove uma coleção existente da lista de coleções do usuário
    
    Raises:
        ValueError: Caso um dos IDs sejam inválidos. Note que os registros podem até existir, mas não significa que estejam associados
    """

    dados = catalogo.carregar()
    for usuario in dados["usuarios"]:
        if usuario["id"] == id_do_usuario:
            if id_da_colecao in usuario["id_colecoes"]:
                usuario["id_colecoes"].remove(id_da_colecao)
                catalogo.salvar(dados)
                return
    raise ValueError("ID da coleção ou ID do usuário inválidos")

            