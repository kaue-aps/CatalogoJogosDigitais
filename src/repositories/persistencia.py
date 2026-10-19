"""
Módulo de persistência em JSON

- Objetivo: desacoplar funções de carregamento e salvamento dos módulos de domínio contidos em src/models

Obs: As regras de negócio serão verificadas no âmbito dos módulos contidos em src/services
"""

import json
from pathlib import Path

class CatalogoJSON:
    def __init__(self, caminho: str):
        self.caminho = Path(caminho)


    def carregar(self):
        # Se o arquivo não existir, retorna o esqueleto da base de dados vazia
        if not self.caminho.exists():
            return {
                "jogos": {
                    "genericos": [],
                    "campanha": [],
                    "competitivo": [],
                    "cooperativo": []
                },
                "usuarios": [],
                "colecoes": []
            }

        with self.caminho.open("r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    def salvar(self, dados: dict):
        with self.caminho.open("w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)