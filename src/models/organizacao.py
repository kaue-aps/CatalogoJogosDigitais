from src.models.jogos import Jogo

class Colecao:
    """Gerencia uma lista de objetos do tipo Jogo"""

    def __init__(self, nome: str, jogos: list[Jogo] = []):
        self.nome = nome
        self.jogos = jogos

    def __str__(self):
        """Retorna um resumo amigável e formatado da coleção em formato de card."""

        titulo = f"\n┌───────────────────── 📂 {self.nome.upper()} ─────────────────────┐\n\n"
        comprimento_titulo = len(f"───────────────────── 📂 {self.nome.upper()} ─────────────────────")

        mensagem = f"{'TÍTULO':<28}{'GÊNERO':<18}{'PLATAFORMA':<14}\n"
        for jogo in self.jogos:
            mensagem += f"🎮 {jogo.titulo:<25}🚩 {jogo.genero:<15}💻 {jogo.plataforma:<12}\n"

        linha_final = f"\n└─{comprimento_titulo * '─'}┘"

        mensagem_final = titulo + mensagem + linha_final

        return mensagem_final


    def __eq__(self, outra_colecao: Colecao) -> bool:
        """Verifica se duas coleções possuem o mesmo nome e os mesmos jogos e se, portanto, são iguais"""

        # Compara com base no nome e sem considerar a ordem dos jogos na lista
        if self.nome == outra_colecao.nome:
            for jogo in self.jogos:
                if jogo not in outra_colecao.jogos:
                    return False
            return True
        else:
            return False

    def __gt__(self, outra_colecao: Colecao) -> bool:
        if len(self.jogos) > len(outra_colecao.jogos):
            return True
        else:
            return False

    def adicionar_jogo(self, jogo: Jogo) -> None:
        """Adiciona um jogo à lista de jogos. Não permite adicionar um jogo já incluído"""
        if jogo not in self.jogos:
            self.jogos.append(jogo)
        else:
            raise ValueError("O mesmo jogo não pode ser adicionado à coleção mais de uma vez")

    def remover_jogo(self, jogo: Jogo) -> None:
        """Remove o jogo da lista de jogos"""
        self.jogos.remove(jogo)

    def listar_jogos(self) -> str:
        """Retorna uma lista enxuta com o nome de todos os jogos da coleção por ordem de inserção"""

        nome_da_colecao_com_espaco = f" {self.nome} "
        mensagem = f"{nome_da_colecao_com_espaco:=^48}\n"
        for jogo in self.jogos:
            mensagem += f"{jogo.titulo:^48}\n"

        return mensagem
        

class Usuario:
    """Pode possuir vários objetos do tipo Colecao associados"""
    pass