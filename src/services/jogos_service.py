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


def cadastrar_jogo(jogo: Jogo | JogoCampanha | JogoCompetitivo | JogoCooperativo):
    dados = catalogo.carregar()

    if isinstance(jogo, Jogo):
        for jogo_cadastrado in dados["jogos"]["genericos"]:
            # Faz a comparação com base nos parâmetros do método __eq__ definido na classe de domínio
            if jogo == Jogo.from_dict(jogo_cadastrado):
                raise PermissionError("O jogo informado já está cadastrado na base de dados")
        jogo.id = proximo_id_jogos()
        dados["jogos"]["genericos"].append(jogo.to_dict())
        catalogo.salvar(dados)

    elif isinstance(jogo, JogoCampanha):
        for jogo_cadastrado in dados["jogos"]["campanha"]:
            if jogo == JogoCampanha.from_dict(jogo_cadastrado):
                raise PermissionError("O jogo informado já está cadastrado na base de dados")
        jogo.id = proximo_id_jogos()
        dados["jogos"]["campanha"].append(jogo.to_dict())
        catalogo.salvar(dados)

    elif isinstance(jogo, JogoCompetitivo):
        for jogo_cadastrado in dados["jogos"]["competitivo"]:
            if jogo == JogoCompetitivo.from_dict(jogo_cadastrado):
                raise PermissionError("O jogo informado já está cadastrado na base de dados")
        jogo.id = proximo_id_jogos()
        dados["jogos"]["competitivo"].append(jogo.to_dict())
        catalogo.salvar(dados)

    elif isinstance(jogo, JogoCooperativo):
        for jogo_cadastrado in dados["jogos"]["cooperativo"]:
            if jogo == JogoCooperativo.from_dict(jogo_cadastrado):
                raise PermissionError("O jogo informado já está cadastrado na base de dados")
        jogo.id = proximo_id_jogos()
        dados["jogos"]["cooperativo"].append(jogo.to_dict())
        catalogo.salvar(dados)

    else:
        raise TypeError("Tipo de jogo informado inválido")


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
        for jogo in categoria: # Percorre a lista de jogos da categoria
            if jogo["id"] == id: # Se o id do jogo for correspondente retorna-se uma instância dele
                if categoria == dados["jogos"]["genericos"]:
                    return Jogo.from_dict(jogo)
                elif categoria == dados["jogos"]["campanha"]:
                    return JogoCampanha.from_dict(jogo)
                elif categoria == dados["jogos"]["competitivo"]:
                    return JogoCompetitivo.from_dict(jogo)
                elif categoria == dados["jogos"]["cooperativo"]:
                    return JogoCooperativo.from_dict(jogo)
                
    raise ValueError("ID do jogo não encontrado.")


def avaliar_jogo(id: int, nota: float) -> None:
    dados = catalogo.carregar()
    for categoria in dados["jogos"].values():
        for jogo in categoria:
            if jogo["id"] == id:
                if categoria == dados["jogos"]["genericos"]:
                    jogo_objeto = Jogo.from_dict(jogo)
                elif categoria == dados["jogos"]["campanha"]:
                    jogo_objeto = JogoCampanha.from_dict(jogo)
                elif categoria == dados["jogos"]["competitivo"]:
                    jogo_objeto =  JogoCompetitivo.from_dict(jogo)
                elif categoria == dados["jogos"]["cooperativo"]:
                    jogo_objeto = JogoCooperativo.from_dict(jogo)

                jogo_objeto.avaliar_jogo(nota) # Validação já embutida no método
                jogo["avaliacao"] = jogo_objeto.avaliacao
                catalogo.salvar(dados)

    raise ValueError("ID do jogo não encontrado.")


