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
