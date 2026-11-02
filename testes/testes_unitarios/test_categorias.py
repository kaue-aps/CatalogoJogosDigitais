"""Módulo com testes unitários para as subclasses de Jogo"""

from src.models.categorias import *

import pytest

# ===================================================================================================
# TESTES JOGOS CAMPANHA
# ===================================================================================================

@pytest.mark.parametrize("capitulos_totais", [-1, 0, 5])
def test_cria_jogo_campanha(capitulos_totais):
    if capitulos_totais >= 1:
        jca1 = JogoCampanha("Batman", "Ação", "Console", capitulos_totais)
        assert jca1._capitulos_totais == capitulos_totais
        assert jca1._capitulos_concluidos == 0

    else:
        with pytest.raises(ValueError):
            jca1 = JogoCampanha("Batman", "Ação", "Console", capitulos_totais)


@pytest.mark.parametrize("capitulos", [-1, 0, 5, 6, 8, 10, 11])
def test_percentual_de_conclusao(capitulos):
    jca1 = JogoCampanha("Batman", "Ação", "Console", 10)
    if capitulos >= 1:
        jca1.avancar_capitulo(capitulos)
        assert jca1.capitulos_concluidos == capitulos
        assert jca1.percentual_conclusao == capitulos / 10 * 100

    else:
        with pytest.raises(ValueError):
            jca1.avancar_capitulo(capitulos)

# ===================================================================================================
# TESTES JOGOS COMPETITIVOS
# ===================================================================================================

def test_taxa_de_vitoria():
    jct1 = JogoCompetitivo("CS-GO", "FPS", "PC")
    jct1.registrar_partida("vitoria")
    jct1.registrar_partida("vitoria")
    jct1.registrar_partida("vitoria")
    jct1.registrar_partida("derrota")

    assert jct1.taxa_vitoria == 75.0

# ===================================================================================================
# TESTES JOGOS COOPERATIVOS
# ===================================================================================================

@pytest.mark.parametrize("max_jogadores", [-1, 0, 1, 2, 10])
def test_cria_jogo_cooperativo(max_jogadores):
    if max_jogadores >= 2:
        jco1 = JogoCooperativo("BuildCoops", "Construção", "PC", max_jogadores)
        assert jco1._max_jogadores == max_jogadores
        assert jco1._sessoes_coop == 0
        assert jco1._participantes_frequentes == []
    else:
        with pytest.raises(ValueError):
            jco1 = JogoCooperativo("BuildCoops", "Construção", "PC", max_jogadores)
