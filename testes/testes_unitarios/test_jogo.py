"""Módulo de testes unitários para a classe Jogo (jogos genéricos)"""

from src.models.jogo import Jogo

from datetime import date
import pytest


@pytest.fixture
def jogo_em_progresso():
    j1 = Jogo("Doom", "FPS", "PC")
    
    j1.registrar_progresso(3)

    return j1

@pytest.fixture
def jogo_finalizado(jogo_em_progresso):
    jogo_em_progresso.finalizar_jogo()
    return jogo_em_progresso

# ===================================================================================================
# TESTES COM CASOS FELIZES E ERROS
# ===================================================================================================

def test_altera_status_e_contabiliza_horas_ao_registrar_progresso():
    j1 = Jogo("Doom", "Ação", "PC")

    j1.registrar_progresso(3)

    assert j1._horas_jogadas == 3
    assert j1._status == "JOGANDO"


def test_armazena_avaliacao_ao_avaliar_jogo(jogo_finalizado):
    jogo_finalizado.avaliar_jogo(10)

    assert jogo_finalizado.avaliacao == 10


def test_altera_estado_do_jogo_ao_finalizar_jogo(jogo_em_progresso):
    jogo_em_progresso.finalizar_jogo()

    assert jogo_em_progresso.status == "FINALIZADO"
    assert jogo_em_progresso._data_termino == date.today()


def test_altera_estado_do_jogo_ao_reiniciar_jogo(jogo_finalizado):
    jogo_finalizado.reiniciar_jogo()

    assert jogo_finalizado.status == "JOGANDO"
    assert jogo_finalizado._horas_jogadas == 0
    assert jogo_finalizado._data_inicio == date.today()


def test_igualdade_entre_jogos(jogo_em_progresso):
    j2 = Jogo("doom", "fps", "pc")

    assert jogo_em_progresso == j2


def test_erro_ao_avaliar_jogo_não_finalizado(jogo_em_progresso):
    with pytest.raises(PermissionError):
        jogo_em_progresso.avaliar_jogo(8.5)


def test_erro_ao_finalizar_jogo_com_menos_de_uma_hora():
    j1 = Jogo("Doom", "FPS", "PC")

    with pytest.raises(PermissionError):
        j1.finalizar_jogo()