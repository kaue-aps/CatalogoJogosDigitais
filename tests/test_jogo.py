# Manipulação abaixo possiblita importar somente as classes que eu quero sem emitir ModuleNotFoundError
import sys
from pathlib import Path

raiz_do_projeto = Path(__file__).parent.parent
if str(raiz_do_projeto) not in sys.path:
    sys.path.append(str(raiz_do_projeto))

# Agora sim posso importar só o que eu quero sem precisar ficar fazendo referência na hora de usar
from src.models.jogos import Jogo

def test_registro_de_progresso():
    j1 = Jogo("Doom", "Ação", "PC")

    j1.registrar_progresso(3)

    assert j1._horas_jogadas == 3
    assert j1.status == "JOGANDO"

def test_finalizar_jogo():
    j1 = Jogo("Doom", "Ação", "PC")

    j1.registrar_progresso(2)
    j1.finalizar_jogo()

    assert j1.status == "FINALIZADO"
    assert j1._horas_jogadas >= 1

def test_avaliar_jogo():
    j1 = Jogo("Doom", "Ação", "PC")

    j1.registrar_progresso(2)
    j1.finalizar_jogo()
    j1.avaliar_jogo(10)

    assert j1.avaliacao == 10