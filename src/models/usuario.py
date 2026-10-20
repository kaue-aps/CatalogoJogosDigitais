"""Módulo contendo a classe Usuario que permite gerenciar coleções"""

from src.models.colecao import Colecao
import src.services.colecao_service as servico_colecao

class Usuario:
    """Representa um usuário do catálogo que pode possuir e administrar suas coleções de jogos

    Attributes:
        nome (str): Nome ou nickname do usuário (case-sensitive)
        colecoes (dict[str, Colecao]): Dicionário de coleções do usuário com o par chave-valor sendo 'nome da coleção - objeto'
    """

    def __init__(self, nome: str, colecoes: list[Colecao] = {}):
        if nome == "":
            raise ValueError("O nome do usuário não pode ser vazio.")
        else:
            self.nome = nome

        self.colecoes = colecoes
        self.id = None

    def __eq__(self, outro_usuario: Usuario) -> bool:
        """Verifica se dois usuários possuem o mesmo nome e as mesmas coleções e se, portanto, são iguais"""

        # Compara com base no nome do usuario e sem considerar a ordem das colecoes
        if self.nome == outro_usuario.nome:
            for colecao in self.colecoes:
                if colecao not in outro_usuario.colecoes:
                    return False
            return True
        else:
            return False

    def __gt__(self, outro_usuario: Usuario) -> bool:
        """Verifica se um usuário é 'maior' do que outro com base no número de coleções"""

        if len(self.colecoes) > len(outro_usuario.colecoes):
            return True
        else:
            return False

    def __str__(self):
        """Retorna um resumo amigável do usuário e de suas coleções"""

        titulo = f"\n┌────────────────── 🥸 {self.nome.upper()} ──────────────────┐\n\n"
        comprimento_titulo = len(f"────────────────── 🥸 {self.nome.upper()} ──────────────────")

        mensagem = f"📗 QUANTIDADE DE COLEÇÕES: {len(self.colecoes)}\n"
        mensagem += f"👾 TOTAL DE JOGOS: "

        qtd_jogos = 0
        for colecao in self.colecoes:
            for jogo in colecao.jogos:
                qtd_jogos += 1

        mensagem += str(qtd_jogos) + "\n"

        linha_final = f"\n└─{comprimento_titulo * '─'}┘"
        mensagem_final = titulo + mensagem + linha_final

        return mensagem_final

    def __repr__(self):
        """Retorna uma mensagem técnica para o desenvolvedor com fins de depuração"""

        return f"Usuario(nome={self.nome!r}, colecoes={self.colecoes!r}, id={self.id!r})"

    def adicionar_colecao(self, colecao: Colecao):
        """Adiciona um objeto Colecao à lista de coleções.

        Args:
            colecao (Colecao): objeto do tipo Colecao

        Raises:
            ValueError: caso nome_colecao seja vazio
            PermissionError: ao tentar adicionar uma coleção que já consta no dicionário

        Returns:
            Colecao: objeto instanciado
        """

        if colecao in self.colecoes:
            raise PermissionError("A coleção já está vinculada ao usuário")
        else:
            self.colecoes.append(colecao)


    def listar_colecoes(self) -> str:
        """Retorna uma string enxuta com o nome de todas as coleções do usuário por ordem de inserção"""

        nome_do_usuario_com_espaco = f" {self.nome} "
        mensagem = f"{nome_do_usuario_com_espaco:=^48}\n"

        for colecao in self.colecoes:
            mensagem += f"{colecao.nome:^48}\n"

        return mensagem


    def remover_colecao(self, id_da_colecao: int) -> None:
        """Exclui uma coleção do usuário

        Args:
            id_da_colecao (int): identificador único da coleção
        
        Raises:
            ValueError: caso o nome da coleção seja inválido (vazio)
            KeyError: caso o nome da coleção não conste no dicionário"""

        for colecao in self.colecoes:
            if colecao.id == id_da_colecao:
                self.colecoes.remove(colecao)
                return

        raise ValueError("ID da coleção não encontrado")


    def to_dict(self):
        return {
            "nome": self.nome,
            "id_colecoes": [colecao.id for colecao in self.colecoes],
            "id": self.colecoes
        }

    @classmethod
    def from_dict(cls, dados):
        usuario = Usuario(dados["nome"], [servico_colecao.get_by_id(id) for id in dados["id_colecoes"]])
        usuario.id = dados["id"]

        return usuario