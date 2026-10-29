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

def redefinir_meta_anual(nova_meta: int) -> None:
    """Redefine a meta anual de jogos finalizados do usuário"""

    if nova_meta < 0:
        raise ValueError("A meta anual não pode ser negativa")
    else:
        config = configuracoes.carregar()
        config["meta_anual_jogos_finalizados"] = nova_meta
        configuracoes.salvar(config)

def redefinir_plataforma_principal(nova_plataforma: str) -> None:
    """Muda a preferência de plataforma do usuário"""

    nova_plataforma = nova_plataforma.strip().upper()
    if nova_plataforma in ["PC", "CONSOLE", "MOBILE"]:
        config = configuracoes.carregar()
        config["plataforma_principal"] = nova_plataforma
        configuracoes.salvar(config)
    else:
        raise ValueError("Plataforma informada é inválida")

def redefinir_generos_favoritos(generos: list[str]) -> None:
    """Redefine os gêneros favoritos do usuário"""

    if len(generos) > 3:
        raise PermissionError("Não é possível definir mais que 3 gêneros favoritos")
    else:
        config = configuracoes.carregar()
        config["generos_favoritos"] = generos
        configuracoes.salvar(config)

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


def limite_jogos_andamento_atingido() -> bool:
    """Retorna True se o número de jogos cadastrados com status 'JOGANDO' for igual ao limite estabelecido
    
    É útil para saber se um novo jogo poderá ser iniciado (registrar_progresso)"""

    config = configuracoes.carregar()
    dados = catalogo.carregar()
    em_andamento = 0

    for lista in dados["jogos"].values:
        for jogo in lista:
            if jogo["status"] == "JOGANDO":
                em_andamento += 1

    if em_andamento == config["limite_jogos_andamento"]:
        return True
    else:
        return False

def configuracoes_atuais() -> str:
    """Retorna o estado atual das configurações em settings.json"""

    config = configuracoes.carregar()
    return (
            f"Gêneros favoritos: {config["generos_favoritos"] if config["generos_favoritos"] != [] else 'Não definido'}\n"
            f"Meta anual de jogos finalizados: {config["meta_anual_jogos_finalizados"]}\n"
            f"{'⚠️ Seu progresso está ABAIXO DA META\n' if not verificar_meta_anual_finalizados() else ''}"
            f"Limite de jogos em andamento: {config["limite_jogos_andamento"]}\n"
            f"Plataforma principal: {config["plataforma_principal"] if config["plataforma_principal"] is not None else 'Não definido'}"
            )
