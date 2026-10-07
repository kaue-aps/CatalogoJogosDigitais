from src.models.colecao import Colecao
from src.models.jogos import Jogo
import pytest

@pytest.fixture
def colecao_cheia():
    r1 = Jogo("RDR 2", "Ação", "Console")
    g1 = Jogo("GTA VI", "Ação", "Console")
    m1 = Jogo("Minecraft", "Sandbox", "PC")
    t1 = Jogo("Terraria", "Aventura", "Mobile")
    f1 = Jogo("Forza", "Corrida", "PC")
    p1 = Jogo("PUBG", "Battle Royale", "Mobile")

    c1 = Colecao("Meus Games Favoritos", [r1, g1, m1, t1, f1, p1])

    return c1

def test_erro_ao_adicionar_mesmo_jogo_na_colecao(colecao_cheia):
    r2 = Jogo("RDR 2", "Ação", "Console")
    
    with pytest.raises(ValueError):
        colecao_cheia.adicionar_jogo(r2)