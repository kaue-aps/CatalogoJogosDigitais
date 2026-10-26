"""Módulo contendo a classe Usuario que permite gerenciar coleções"""

from src.models.colecao import Colecao
import src.services.colecao_service as servico_colecao

class Usuario:
    """Representa o usuário principal do catálogo que pode possuir e administrar suas coleções de jogos

    Attributes:
        nome (str): Nome ou nickname do usuário (case-sensitive)
        colecoes (list[Colecao]): Lista de objetos coleção do usuário
    """

    def __init__(self, nome: str, colecoes: list[Colecao] = []):
        if nome == "":
            raise ValueError("O nome do usuário não pode ser vazio.")
        else:
            self._nome = nome

        self._colecoes = colecoes
        self._id = None


    def __str__(self):
        """Retorna um resumo amigável do usuário e de suas coleções"""

        titulo = f"\n┌────────────────── 🥸 {self._nome.upper()} ──────────────────┐\n\n"
        comprimento_titulo = len(f"────────────────── 🥸 {self._nome.upper()} ──────────────────")

        mensagem = f"📗 QUANTIDADE DE COLEÇÕES: {len(self._colecoes)}\n"
        mensagem += f"👾 TOTAL DE JOGOS: "

        qtd_jogos = 0
        for colecao in self._colecoes:
            for jogo in colecao._jogos:
                qtd_jogos += 1

        mensagem += str(qtd_jogos) + "\n"

        linha_final = f"\n└─{comprimento_titulo * '─'}┘"
        mensagem_final = titulo + mensagem + linha_final

        return mensagem_final


    def __repr__(self):
        """Retorna uma mensagem técnica para o desenvolvedor com fins de depuração"""

        return f"Usuario(nome={self._nome!r}, colecoes={self._colecoes!r}, id={self._id!r})"


    def adicionar_colecao(self, colecao: Colecao) -> None:
        """Adiciona um objeto Colecao à lista de coleções.

        Args:
            colecao (Colecao): objeto Colecao

        Raises:
            PermissionError: ao tentar adicionar uma coleção que já consta na lista
        """

        # Invoca o método __eq__ de Colecao implicitamente para verificar a pertinência com base nos critérios estabelecidos
        if colecao in self._colecoes:
            raise PermissionError("A coleção já está vinculada ao usuário")
        else:
            self._colecoes.append(colecao)


    def listar_colecoes(self) -> str:
        """Retorna uma string vertical enxuta com o nome de todas as coleções do usuário por ordem de inserção"""

        nome_do_usuario_com_espaco = f" {self._nome} "
        mensagem = f"{nome_do_usuario_com_espaco:=^48}\n"

        for colecao in self._colecoes:
            mensagem += f"{colecao._nome:^48}\n"

        return mensagem


    def remover_colecao(self, id_da_colecao: int) -> None:
        """Exclui uma coleção da lista do usuário com base no ID

        Args:
            id_da_colecao (int): identificador único da coleção
        
        Raises:
            ValueError: caso o ID informado não corresponda a nenhuma coleção
        """

        for colecao in self._colecoes:
            if colecao._id == id_da_colecao:
                self._colecoes.remove(colecao)
                return

        raise ValueError("ID da coleção não encontrado")


    # Serialização para compatibilidade com JSON
    def to_dict(self):
        return {
            "nome": self._nome,
            "id_colecoes": [colecao._id for colecao in self._colecoes], # Não pode armazenar objetos Colecao em JSON, por isso armazena os IDs
            "id": self._id
        }

    # Desserialização a partir dos dados do JSON
    @classmethod
    def from_dict(cls, dados):
        usuario = Usuario(dados["nome"], [servico_colecao.get_by_id(id) for id in dados["id_colecoes"]]) # Instancia um usuário pelos parâmetros: (1) Nome; (2) Lista de coleções obtidas pelo ID
        usuario._id = dados["id"]

        return usuario