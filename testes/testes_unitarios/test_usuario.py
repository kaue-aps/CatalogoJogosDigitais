"""Módulo para testes unitários da classe Usuario"""

from src.models.usuario import Usuario
from src.models.colecao import Colecao

def test_criar_usuario():
    u1 = Usuario("Godofredo")

    assert u1._colecoes == []
    assert u1._id == None
    assert u1._nome == "Godofredo"


def test_add_e_remove_colecao():
    c1 = Colecao("Jogos 2026")
    c2 = Colecao("Jogos 2025")
    c3 = Colecao("Jogos 2024")

    u1 = Usuario("Godofredo", [c1, c2])
    u1.adicionar_colecao(c3)
    u1.remover_colecao(c1)

    assert u1.listar_colecoes() == f"{' Godofredo ':=^48}\n{'Jogos 2025':^48}\n{'Jogos 2024':=^48}\n"

