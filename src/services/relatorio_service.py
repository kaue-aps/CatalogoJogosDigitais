"""
Serviços de Relatório

Responsabilidades:
- Calcular estatísticas básicas do catálogo
- Fazer consultas simples e buscas filtradas
"""

from src.repositories.persistencia import CatalogoJSON
from src.models.jogo import Jogo
from src.models.categorias import JogoCampanha, JogoCompetitivo, JogoCooperativo

catalogo = CatalogoJSON("data/catalogo.json")

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
    for categoria in dados["jogos"]:
        for jogo in categoria:
            if jogo["avaliacao"] is not None:
                soma += jogo["avaliacao"]
                qtd += 1

    media = soma / qtd
    return media

def percentual_de_jogos_por_status() -> dict:
    dados = catalogo.carregar()
    nao_iniciados = jogando = finalizados = 0
    total_jogos = 0
    for categoria in dados["jogos"]:
            for jogo in categoria:
                if jogo["status"] == "NÃO INICIADO":
                    nao_iniciados += 1
                elif jogo["status"] == "JOGANDO":
                    jogando += 1
                elif jogo["status"] == "FINALIZADO":
                    finalizados += 1

                total_jogos += 1

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
    for categoria in dados["jogos"]:
        for jogo in categoria:
            todos_jogos.extend(jogo) # Vai adicionando os jogos em forma de dicionário à lista

    jogos_em_ordem_descrescente = sorted(todos_jogos,
                                        key=lambda jogo: jogo["horas_jogadas"],
                                        reverse=True)
    
    top_5_lista = jogos_em_ordem_descrescente[:5] # Pega os primeiros cinco usando fatiamento de string

    top_5_dict = {} # Dicionário do top 5 com chaves em números ordinais

    # Loop que coloca os jogos já instanciados em top_5_dict
    for i in range(0, 5):
        jogo = top_5_lista[i]

        # Verificação para instanciar corretamente a depender da categoria do jogo
        if jogo in dados["jogos"]["genericos"]:
            top_5_dict[f"{i + 1}º"] = Jogo.from_dict(jogo)

        elif jogo in dados["jogos"]["campanha"]:
            top_5_dict[f"{i + 1}º"] = JogoCampanha.from_dict(jogo)

        elif jogo in dados["jogos"]["competitivo"]:
            top_5_dict[f"{i + 1}º"] = JogoCompetitivo.from_dict(jogo)

        elif jogo in dados["jogos"]["cooperativo"]:
            top_5_dict[f"{i + 1}º"] = JogoCooperativo.from_dict(jogo)

    return top_5_dict
