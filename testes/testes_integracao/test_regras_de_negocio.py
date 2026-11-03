# Módulo para testes das regras de negócio principais a nível de banco de dados

import src.repositories.persistencia as persistencia
import src.repositories.config as config

import src.services.jogos_service as servico_jogos
import src.services.configuracao_service as servico_configuracoes

from src.models.jogo import Jogo
from src.models.categorias import *

import pytest

# Para viabilizar os testes de persistência em um arquivo JSON temporário, tive que usar
# Monkeypatch: fixture nativa que permite mudar uma variável global de outro módulo apenas durante o teste
# tmp_path: fixture nativa que cria um arquivo temporário

def test_cadastrar_jogo(monkeypatch, tmp_path):
    monkeypatch.setattr(persistencia, "caminho_padrao", str(tmp_path / "catalogo_temp.json"))
    arquivo_temp = tmp_path / "catalogo_temp.json"
    monkeypatch.setattr(servico_jogos.catalogo, "caminho", arquivo_temp)
    j1 = Jogo("Doom", "FPS", "PC")

    servico_jogos.cadastrar_jogo(j1)
    
    catalogo = persistencia.CatalogoJSON(str(tmp_path / "catalogo_temp.json"))
    dados = catalogo.carregar()

    assert j1.to_dict() in dados["jogos"]["genericos"]
    assert j1.id == 1
    assert j1.horas_jogadas == 0


def test_erro_jogo_duplicado(monkeypatch, tmp_path):
    monkeypatch.setattr(persistencia, "caminho_padrao", str(tmp_path / "catalogo_temp.json"))
    arquivo_temp = tmp_path / "catalogo_temp.json"
    monkeypatch.setattr(servico_jogos.catalogo, "caminho", arquivo_temp)
    servico_jogos.cadastrar_jogo(Jogo("Doom", "FPS", "PC"))

    with pytest.raises(PermissionError):
        servico_jogos.cadastrar_jogo(Jogo("doom", "rpg", "pc"))


def test_erro_ao_avaliar_jogo_antes_de_finalizar(monkeypatch, tmp_path):
    monkeypatch.setattr(persistencia, "caminho_padrao", str(tmp_path / "catalogo_temp.json"))
    arquivo_temp = tmp_path / "catalogo_temp.json"
    monkeypatch.setattr(servico_jogos.catalogo, "caminho", arquivo_temp)
    servico_jogos.cadastrar_jogo(Jogo("Doom", "FPS", "PC"))

    with pytest.raises(PermissionError):
        servico_jogos.avaliar_jogo(1, 9.5)


def test_registro_de_progresso(monkeypatch, tmp_path):
    monkeypatch.setattr(persistencia, "caminho_padrao", str(tmp_path / "catalogo_temp.json"))
    arquivo_temp = tmp_path / "catalogo_temp.json"
    monkeypatch.setattr(servico_jogos.catalogo, "caminho", arquivo_temp)
    lista_jogos = [
                    JogoCampanha("RDR 2", "Ação", "Console", 5),      
                    Jogo("GTA VI", "Ação", "Console"),      
                    JogoCooperativo("Minecraft", "Sandbox", "PC", 10)
    ]

    i = 1 # Representa o id e as horas
    for jogo in lista_jogos:
        servico_jogos.cadastrar_jogo(jogo)
        servico_jogos.registrar_progresso(i, i)
        i += 1

    catalogo = persistencia.CatalogoJSON(str(tmp_path / "catalogo_temp.json"))
    dados = catalogo.carregar()

    assert dados["jogos"]["genericos"][0]["horas_jogadas"] == 2
    assert dados["jogos"]["campanha"][0]["horas_jogadas"] == 1
    assert dados["jogos"]["cooperativo"][0]["horas_jogadas"] == 3


def test_erro_mais_de_tres_jogos_em_andamento(monkeypatch, tmp_path):
    monkeypatch.setattr(persistencia, "caminho_padrao", str(tmp_path / "catalogo_temp.json"))
    arquivo_temp = tmp_path / "catalogo_temp.json"
    monkeypatch.setattr(servico_jogos.catalogo, "caminho", arquivo_temp)
    monkeypatch.setattr(servico_configuracoes.catalogo, "caminho", arquivo_temp)
    monkeypatch.setattr(servico_configuracoes.configuracoes, "caminho", tmp_path / "settings_temp.json")
    lista_jogos = [
                    JogoCampanha("RDR 2", "Ação", "Console", 5),      
                    Jogo("GTA VI", "Ação", "Console"),      
                    JogoCooperativo("Minecraft", "Sandbox", "PC", 10)
    ]
    
    i = 1
    for jogo in lista_jogos:
        servico_jogos.cadastrar_jogo(jogo)
        servico_jogos.registrar_progresso(i, i)
        i += 1

    servico_jogos.cadastrar_jogo(JogoCooperativo("Terraria", "Aventura", "Mobile", 10))
    with pytest.raises(PermissionError):
        servico_jogos.registrar_progresso(4, 4)


def test_abaixo_meta_anual_de_jogos_finalizados(monkeypatch, tmp_path):
    monkeypatch.setattr(persistencia, "caminho_padrao", str(tmp_path / "catalogo_temp.json"))
    arquivo_temp = tmp_path / "catalogo_temp.json"
    monkeypatch.setattr(servico_jogos.catalogo, "caminho", arquivo_temp)

    monkeypatch.setattr(config, "caminho_padrao", str(tmp_path / "settings_temp.json"))
    monkeypatch.setattr(servico_configuracoes, "caminho", str(tmp_path / "catalogo_temp.json"))
    monkeypatch.setattr(servico_configuracoes, "caminho_config", str(tmp_path / "settings_temp.json"))
    monkeypatch.setattr(
        servico_configuracoes.catalogo,
        "caminho",
        tmp_path / "catalogo_temp.json",
    )
    monkeypatch.setattr(
        servico_configuracoes.configuracoes,
        "caminho",
        tmp_path / "settings_temp.json",
    )
    servico_configuracoes.redefinir_meta_anual(4)
    lista_jogos = [
                    JogoCampanha("RDR 2", "Ação", "Console", 5),      
                    Jogo("GTA VI", "Ação", "Console"),      
                    JogoCooperativo("Minecraft", "Sandbox", "PC", 10)
        ]

    i = 1
    for jogo in lista_jogos:
        servico_jogos.cadastrar_jogo(jogo)
        servico_jogos.registrar_progresso(i, i)
        servico_jogos.finalizar_jogo(i)
        i += 1

    assert servico_configuracoes.verificar_meta_anual_finalizados() is False