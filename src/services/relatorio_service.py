"""
Serviços de Relatório

Responsabilidades:
- Calcular estatísticas básicas do catálogo
- Fazer consultas simples e buscas filtradas
"""

from src.repositories.persistencia import CatalogoJSON
from src.models.jogo import Jogo
from src.models.categorias import JogoCampanha, JogoCompetitivo, JogoCooperativo

caminho = "data/catalogo.json"
catalogo = CatalogoJSON(caminho)

def total_de_jogos_cadastrados() -> int:
    dados = catalogo.carregar()
    jogos_genericos = len(dados["jogos"]["genericos"])
    jogos_campanha = len(dados["jogos"]["campanha"])
    jogos_competitivos = len(dados["jogos"]["competitivo"])
    jogos_cooperativos = len(dados["jogos"]["cooperativo"])

    total = jogos_genericos + jogos_campanha + jogos_competitivos + jogos_cooperativos

    return total

def total_de_horas_jogadas() -> float:
    dados = catalogo.carregar()
    horas_jogadas = 0
    for categoria in dados["jogos"].values():
        for jogo in categoria:
            horas_jogadas += jogo["horas_jogadas"]

    return horas_jogadas

def media_de_avaliacao_jogos() -> float:
    dados = catalogo.carregar()
    soma = qtd = 0
    for jogos_da_categoria in dados["jogos"].values():
        for jogo in jogos_da_categoria:
            if jogo["avaliacao"] is not None:
                soma += jogo["avaliacao"]
                qtd += 1

    return soma / qtd if qtd else 0.0

def percentual_de_jogos_por_status() -> dict:
    dados = catalogo.carregar()
    nao_iniciados = jogando = finalizados = 0
    total_jogos = 0
    for jogos_da_categoria in dados["jogos"].values():
        for jogo in jogos_da_categoria:
            if jogo["status"] == "NÃO INICIADO":
                nao_iniciados += 1
            elif jogo["status"] == "JOGANDO":
                jogando += 1
            elif jogo["status"] == "FINALIZADO":
                finalizados += 1

            total_jogos += 1

    if total_jogos == 0:
        percentual_nao_iniciados = percentual_jogando = percentual_finalizados = 0.0
    else:
        percentual_nao_iniciados = (nao_iniciados / total_jogos) * 100
        percentual_jogando = (jogando / total_jogos) * 100
        percentual_finalizados = (finalizados / total_jogos) * 100

    return {
        "NÃO INICIADO": percentual_nao_iniciados,
        "JOGANDO": percentual_jogando,
        "FINALIZADO": percentual_finalizados
    }

def top_5_jogos_mais_jogados():
    dados = catalogo.carregar()
    todos_jogos = []
    classes_por_categoria = {
        "genericos": Jogo,
        "campanha": JogoCampanha,
        "competitivo": JogoCompetitivo,
        "cooperativo": JogoCooperativo,
    }

    for categoria, jogos_da_categoria in dados["jogos"].items():
        for jogo in jogos_da_categoria:
            todos_jogos.append((categoria, jogo))

    jogos_em_ordem_descrescente = sorted(
        todos_jogos,
        key=lambda item: item[1]["horas_jogadas"],
        reverse=True,
    )

    top_5_dict = {}
    for i, (categoria, dados_jogo) in enumerate(jogos_em_ordem_descrescente[:5], start=1):
        classe_jogo = classes_por_categoria[categoria]
        top_5_dict[f"{i}º"] = classe_jogo.from_dict(dados_jogo)

    return top_5_dict
