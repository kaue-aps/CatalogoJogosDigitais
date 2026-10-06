# Manipulação abaixo possiblita importar somente as classes que eu quero sem emitir ModuleNotFoundError
import sys
from pathlib import Path

raiz_do_projeto = Path(__file__).parent.parent
if str(raiz_do_projeto) not in sys.path:
    sys.path.append(str(raiz_do_projeto))

# Agora sim posso importar só o que eu quero sem precisar ficar fazendo referência de módulo na hora de usar
from src.models.jogos import Jogo

from datetime import date
import pytest

# Predefine um Jogo já iniciado com 3 horas de progresso
@pytest.fixture
def jogo_em_progresso():
    j1 = Jogo("Doom", "FPS", "PC")
    
    j1.registrar_progresso(3)

    return j1

@pytest.fixture
def jogo_finalizado(jogo_em_progresso):
    jogo_em_progresso.finalizar_jogo()
    return jogo_em_progresso

def test_deve_alterar_status_e_contabilizar_horas_ao_registrar_progresso():
    j1 = Jogo("Doom", "Ação", "PC")

    j1.registrar_progresso(3)

    assert j1._horas_jogadas == 3
    assert j1.status == "JOGANDO"

def test_deve_alterar_status_e_verificar_horas_jogadas_finalizar_jogo(jogo_em_progresso):
    jogo_em_progresso.finalizar_jogo()

    assert jogo_em_progresso.status == "FINALIZADO"
    assert jogo_em_progresso._horas_jogadas >= 1

def test_deve_armazenar_avaliacao_ao_avaliar_jogo(jogo_em_progresso):
    jogo_em_progresso.finalizar_jogo()
    jogo_em_progresso.avaliar_jogo(10)

    assert jogo_em_progresso.avaliacao == 10

def test_deve_alterar_status_zerar_horas_e_mudar_datas_ao_reiniciar_jogo(jogo_finalizado):
    jogo_finalizado.reiniciar_jogo()

    assert jogo_finalizado.status == "JOGANDO"
    assert jogo_finalizado._horas_jogadas == 0
    assert jogo_finalizado._data_inicio == date.today()