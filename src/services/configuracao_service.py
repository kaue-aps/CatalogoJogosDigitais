"""
Serviços de Configuração

Responsabilidades:
- Reconfigurar métricas e parâmetros definidos pelo usuário
- Fazer validações com o que consta em settings.json
"""

from src.repositories.config import ConfiguracaoJSON
from src.repositories.persistencia import CatalogoJSON

configuracoes = ConfiguracaoJSON("data/settings.json")
catalogo = CatalogoJSON("data/catalogo.json")


def verificar_meta_anual_finalizados() -> bool:
    """Retorna True se a quantidade de jogos finalizados for maior ou igual à meta estabelecida nas configurações"""

    config = configuracoes.carregar()
    dados = catalogo.carregar()

    finalizados = 0
    for lista in dados["jogos"].values():
        for jogo in lista:
            if jogo["status"] == "FINALIZADO":
                finalizados += 1

    if finalizados >= config["meta_anual_jogos_finalizados"]:
        return True
    else:
        return False


def redefinir_limite_jogos_andamento(novo_limite: int) -> None:
    """Muda o limite de jogos com status 'JOGANDO'

    Se o limite for reduzido e houver mais jogos em andamento do que o permitido esses jogos não serão afetados

    Args:
        novo_limite (int): pode ser maior ou menor do que o atual, desde que seja >= 1
    """

    if novo_limite <= 1:
        raise ValueError("Deve ser permitido ao menos um jogo em andamento")
    else:
        config = configuracoes.carregar()
        config["limite_jogos_andamento"] = novo_limite
        configuracoes.salvar(config)

def get_limite_jogos_andamento() -> int:
    """Retorna o limite atual de jogos com status 'JOGANDO'"""

    config = configuracoes.carregar()
    return config["limite_jogos_andamento"]

def limite_jogos_andamento_atingido() -> bool:
    """Retorna True se o número de jogos cadastrados com status 'JOGANDO' for igual ao limite estabelecido"""

    dados = catalogo.carregar()
    em_andamento = 0

    for lista in dados["jogos"].values:
        for jogo in lista:
            if jogo["status"] == "JOGANDO":
                em_andamento += 1

    if em_andamento == get_limite_jogos_andamento:
        return True
    else:
        return False

