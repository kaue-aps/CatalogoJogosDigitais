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

        return f"Usuario(nome={self.nome!r}, colecoes={self.colecoes!r})"

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

    def listar_colecoes(self) -> str:
        """Retorna uma string enxuta com o nome de todas as coleções do usuário por ordem de inserção"""

        nome_do_usuario_com_espaco = f" {self.nome} "
        mensagem = f"{nome_do_usuario_com_espaco:=^48}\n"

        # Ao iterar usando o método values(), pegamos o nome 
        # da coleção tal qual como foi criada e não as chaves que são todas minúsculas
        for colecao in self.colecoes.values():
            mensagem += f"{colecao:^48}\n"

        return mensagem

    def deletar_colecao(self, nome_colecao: str) -> None:
        """Exclui uma coleção do usuário de coleções do usuário

        Args:
            nome_colecao (str): é case-insensitive
        
        Raises:
            ValueError: caso o nome da coleção seja inválido (vazio)
            KeyError: caso o nome da coleção não conste no dicionário"""

        nome_limpo = nome_colecao.strip()
        chave = nome_limpo.lower()
        if chave == "":
            raise ValueError("Nome de coleção inválido (vazio)")
        
        if chave not in self.colecoes:
            raise KeyError(f"A coleção {nome_limpo} não consta na lista de coleções")

        del self.colecoes[chave]