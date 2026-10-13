"""Módulo contendo a classe Usuario que permite gerenciar coleções"""

from src.models.colecao import Colecao


class Usuario:
    """Representa um usuário do catálogo que pode possuir e administrar suas coleções de jogos

    Attributes:
        nome (str): Nome ou nickname do usuário (case-sensitive)
        colecoes (dict[str, Colecao]): Dicionário de coleções do usuário com o par chave-valor sendo 'nome da coleção - objeto'
    """

    def __init__(self, nome: str, colecoes: dict[str, Colecao] = {}):
        if nome == "":
            raise ValueError("O nome do usuário não pode ser vazio.")
        else:
            self.nome = nome

        self.colecoes = colecoes

    def criar_colecao(self, nome_colecao: str) -> Colecao:
        """Adiciona uma nova coleção ao dicionário de coleções.

        Args:
            nome_colecao (str): é case-insensitive

        Raises:
            ValueError: caso nome_colecao seja vazio
            PermissionError: ao tentar adicionar uma coleção que já consta no dicionário

        Returns:
            Colecao: objeto instanciado
        """

        nome_limpo = nome_colecao.strip()
        chave = nome_limpo.lower()
        if chave == "":
            raise ValueError("O nome da coleção não pode ser vazio")

        if chave in self.colecoes:
            raise PermissionError(f"A coleção {chave} já está na lista de coleções")

        nova_colecao = Colecao(nome_limpo)
        self.colecoes[chave] = nova_colecao

        return nova_colecao

    def obter_colecao(self, nome_colecao: str) -> Colecao:
        """Retorna um objeto do tipo Colecao caso esteja no dicionário de coleções

        Args:
            nome_colecao (str): é case-insensitive

        Raises:
            ValueError: caso o nome da coleção seja inválido (vazio)
            KeyError: caso o nome da coleção não conste no dicionário
        """

        nome_limpo = nome_colecao.strip()
        chave = nome_limpo.lower()
        if chave == "":
            raise ValueError("Nome de coleção inválido (vazio)")
        
        if chave not in self.colecoes:
            raise KeyError(f"A coleção {nome_limpo} não consta na lista de coleções")

        colecao = self.colecoes[chave]
        return colecao
        