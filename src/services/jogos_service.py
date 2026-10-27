"""
Serviços de Jogos

Contém funções específicas para jogos genéricos ou de categoria

Responsabilidades:
- Orquestrar o CRUD básico de jogos
- Garantir regras de negócio ao manipular esses jogos
- Filtrar e ordenar buscas de jogos
"""

from src.repositories.persistencia import CatalogoJSON
from src.services.configuracao_service import limite_jogos_andamento_atingido
from src.models.jogo import Jogo
from src.models.categorias import *

catalogo = CatalogoJSON("data/catalogo.json")


def proximo_id_jogos() -> int:
    """Retorna o próximo do id do jogo a ser cadastrado com base no maior id existente na base de dados"""

    dados = catalogo.carregar()
    maior = 0 # Começa em 0 para que o retorno mínimo (maior + 1) seja 1

    for categoria in dados["jogos"].values():
        # Só vamos olhar para categorias que têm jogos
        if categoria:
            maximo_da_categoria = max(jogo["id"] for jogo in categoria)
            if maximo_da_categoria > maior:
                maior = maximo_da_categoria

    return maior + 1


def cadastrar_jogo(jogo: Jogo | JogoCampanha | JogoCompetitivo | JogoCooperativo) -> None:
    """Persiste um jogo na base de dados, agindo polimorficamente dependendo da categoria informada"""

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


def deletar_jogo(id: int) -> None:
    """Exclui um jogo da base de dados conforme id especificado"""

    dados = catalogo.carregar()
    for categoria in dados["jogos"].values():
        for jogo in categoria:
            if jogo["id"] == id:
                categoria.remove(jogo)
                catalogo.salvar(dados)
                return
    raise ValueError("ID do jogo não encontrado.")


def get_by_id(id: int) -> Jogo | JogoCampanha | JogoCompetitivo | JogoCooperativo:
    """Retorna o jogo instanciado com id correspondente na base de dados"""

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


def atualizar_jogo(id: int, dados_atualizados: dict) -> None:
    """Atualiza o estado de um jogo na base de dados JSON.
    
    Somente os dados modificados precisam ser passados como parâmetro.

    Args:
        id (int): id do jogo
        dados_atualizados (dict): chaves (atributos) e valores a serem modificados. Ex: {"avaliacao": x, "status": y}
    """

    dados = catalogo.carregar()
    
    for categoria, lista_jogos in dados["jogos"].items():
        for jogo in lista_jogos:
            if jogo["id"] == id:
                # Impede que o ID seja alterado acidentalmente via update
                if "id" in dados_atualizados:
                    del dados_atualizados["id"]
                    
                # Atualiza os campos do dicionário existente
                jogo.update(dados_atualizados)
                
                # Valida se as novas chaves/valores não quebram o contrato da classe
                try:
                    if categoria == "genericos":
                        Jogo.from_dict(jogo)
                    elif categoria == "campanha":
                        JogoCampanha.from_dict(jogo)
                    elif categoria == "competitivo":
                        JogoCompetitivo.from_dict(jogo)
                    elif categoria == "cooperativo":
                        JogoCooperativo.from_dict(jogo)
                except Exception as e:
                    raise ValueError(f"Os dados fornecidos são inválidos para instanciar o jogo: {e}")

                catalogo.salvar(dados)
                return
                
    raise ValueError("ID do jogo não encontrado.")

def registrar_progresso(id: int, horas: float) -> None:
    """Adiciona horas de gameplay a um jogo, podendo alterar seu status e sua data de início.
    
    Raises:
        PermissionError: caso o limite de jogos em andamento já tenha sido atingido no catálogo
    """

    jogo_cadastrado = get_by_id(id)

    # Regra de Negócio: não podemos exceder o limite de jogos com status "JOGANDO"
    if jogo_cadastrado._status != "JOGANDO":
        if limite_jogos_andamento_atingido():
            return PermissionError("De acordo com as configurações do sistema, não são permitidos mais de 3 jogos com status 'JOGANDO'")
    # Caso o usuário já esteja jogando, prossiga normalmente
    jogo_cadastrado.registrar_progresso(horas) # Validação embutida no método
    # Atualiza apenas os atributos que podem ter sido eventualmente mudados
    atualizar_jogo(id, {"horas_jogadas": jogo_cadastrado.horas_jogadas,
                        "data_inicio": jogo_cadastrado.data_inicio,
                        "status": jogo_cadastrado._status})
    

def avaliar_jogo(id: int, nota: float) -> None:
    """Persiste uma avaliação do jogo de forma validada"""

    jogo_objeto = get_by_id(id)
    jogo_objeto.avaliar_jogo(nota) # Validação já embutida no método
    
    atualizar_jogo(id, {"avaliacao": jogo_objeto.avaliacao}) # Persistência


def listar_jogos() -> list:
    """Retorna todos os jogos do catalogo de forma instanciada em uma lista"""
    dados = catalogo.carregar()
    jogos_encontrados = []
    
    for categoria, lista_jogos in dados["jogos"].items():
        for jogo in lista_jogos:
            if categoria == "genericos":
                jogos_encontrados.append(Jogo.from_dict(jogo))
            elif categoria == "campanha":
                jogos_encontrados.append(JogoCampanha.from_dict(jogo))
            elif categoria == "competitivo":
                jogos_encontrados.append(JogoCompetitivo.from_dict(jogo))
            elif categoria == "cooperativo":
                jogos_encontrados.append(JogoCooperativo.from_dict(jogo))
                
    return jogos_encontrados


def listar_por_genero(genero: str) -> list:
    """Retorna uma lista filtrada de objetos Jogo ou subclasses do gênero correspondente ao informado"""

    dados = catalogo.carregar()
    jogos_encontrados = []
    
    genero_busca = genero.strip().lower() # Busca padronizada em minúsculas sem espaços
    
    for categoria, lista_jogos in dados["jogos"].items():
        for jogo in lista_jogos:
            if jogo["genero"].strip().lower() == genero_busca: # Instancia e adiciona à lista caso seja do gênero correspondente
                if categoria == "genericos":
                    jogos_encontrados.append(Jogo.from_dict(jogo))
                elif categoria == "campanha":
                    jogos_encontrados.append(JogoCampanha.from_dict(jogo))
                elif categoria == "competitivo":
                    jogos_encontrados.append(JogoCompetitivo.from_dict(jogo))
                elif categoria == "cooperativo":
                    jogos_encontrados.append(JogoCooperativo.from_dict(jogo))
                
    return jogos_encontrados


def listar_por_status(status: str) -> list:
    """Retorna uma lista filtrada de objetos Jogo ou subclasses com o status correspondente ao informado"""

    dados = catalogo.carregar()
    jogos_encontrados = []
    
    status_busca = status.strip().lower()
    
    for categoria, lista_jogos in dados["jogos"].items():
        for jogo in lista_jogos:
            if jogo["status"].strip().lower() == status_busca:
                if categoria == "genericos":
                    jogos_encontrados.append(Jogo.from_dict(jogo))
                elif categoria == "campanha":
                    jogos_encontrados.append(JogoCampanha.from_dict(jogo))
                elif categoria == "competitivo":
                    jogos_encontrados.append(JogoCompetitivo.from_dict(jogo))
                elif categoria == "cooperativo":
                    jogos_encontrados.append(JogoCooperativo.from_dict(jogo))
                
    return jogos_encontrados


def listar_por_plataforma(plataforma: str) -> list:
    """Retorna uma lista filtrada de objetos Jogo ou subclasses com a plataforma correspondente à informada"""

    dados = catalogo.carregar()
    jogos_encontrados = []
    
    plataforma_busca = plataforma.strip().lower()
    
    for categoria, lista_jogos in dados["jogos"].items():
        for jogo in lista_jogos:
            if jogo["plataforma"].strip().lower() == plataforma_busca:
                if categoria == "genericos":
                    jogos_encontrados.append(Jogo.from_dict(jogo))
                elif categoria == "campanha":
                    jogos_encontrados.append(JogoCampanha.from_dict(jogo))
                elif categoria == "competitivo":
                    jogos_encontrados.append(JogoCompetitivo.from_dict(jogo))
                elif categoria == "cooperativo":
                    jogos_encontrados.append(JogoCooperativo.from_dict(jogo))
                
    return jogos_encontrados


def buscar_por_titulo(termo: str) -> list:
    """Retorna uma lista de jogos com o termo informado inserido no título (busca parcial)"""

    dados = catalogo.carregar()
    jogos_encontrados = []
    termo_busca = termo.strip().lower()
    
    # Retorna lista vazia se a busca for apenas espaços em branco
    if not termo_busca:
        return jogos_encontrados

    for categoria, lista_jogos in dados["jogos"].items():
        for jogo in lista_jogos:
            titulo_jogo = jogo["titulo"].strip().lower()
            
            # Verifica se o termo pesquisado está contido no título
            if termo_busca in titulo_jogo:
                if categoria == "genericos":
                    jogos_encontrados.append(Jogo.from_dict(jogo))
                elif categoria == "campanha":
                    jogos_encontrados.append(JogoCampanha.from_dict(jogo))
                elif categoria == "competitivo":
                    jogos_encontrados.append(JogoCompetitivo.from_dict(jogo))
                elif categoria == "cooperativo":
                    jogos_encontrados.append(JogoCooperativo.from_dict(jogo))
                
    return jogos_encontrados


def ordenar_jogos_por_avaliacao(reverse: bool = True) -> list:
    """Retorna a lista ordenada dos jogos mais bem avaliados por padrão
    
    Args:
        reverse (bool): piores avaliações primeiro (False) ou mais bem avaliados primeiro (True)
    """
    jogos = listar_jogos()
    # Pega o atributo 'avaliacao' de cada objeto.
    # Usa getattr com default 0.0 caso a avaliação ainda não tenha sido feita
    return sorted(jogos, key=lambda jogo: getattr(jogo, "avaliacao", 0.0), reverse=reverse)


def ordenar_jogos_por_horas_jogadas(reverse: bool = True) -> list:
    """Retorna a lista ordenada dos jogos mais jogados por padrão
    
    Args:
        reverse (bool): menos jogados primeiro (False) ou mais jogados primeiro (True)
    """

    jogos = listar_jogos()
    return sorted(jogos, key=lambda jogo: getattr(jogo, "horas_jogadas"), reverse=reverse)