"""
Módulo de persistência de configurações em JSON

- Objetivo: desacoplar funções de carregamento e salvamento das funções de verificação contidas em src/services/configuracao_service
"""

import json
from pathlib import Path

class ConfiguracaoJSON:
    def __init__(self, caminho: str):
        self.caminho = Path(caminho)

    def carregar(self):
        # Se o arquivo não existir, retorna o esqueleto de configurações vazio
        if not self.caminho.exists():
            return {
                "generos_favoritos": [],
                "meta_anual_jogos_finalizados": 0,
                "limite_jogos_andamento": 3,
                "plataforma_principal": None
            }

        with self.caminho.open("r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    def salvar(self, dados):
        with self.caminho.open("w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
