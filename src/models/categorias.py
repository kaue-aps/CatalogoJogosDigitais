"""Módulo contendo subclasses de Jogo para diferentes experiências de jogatina."""

from src.models.jogo import Jogo

class JogoCampanha(Jogo):
    """Representa um jogo focado em modo história/campanha. É iniciado com 0 capítulos concluídos

    Attributes:
        capitulos_totais (int): Quantidade total de capítulos ou missões (deve ser maior que zero)
        capitulos_concluidos (int): Quantidade de capítulos já concluídos.
    """

    def __init__(self, titulo: str, genero: str, plataforma: str, capitulos_totais: int) -> None:
        super().__init__(titulo, genero, plataforma)

        # Verifica se a quantidade de capítulos totais é nula ou negativa
        if capitulos_totais <= 0:
            raise ValueError("O jogo deve ter pelo menos um capítulo")
        else:
            self._capitulos_totais = capitulos_totais

        self._capitulos_concluidos = 0


    @property
    def capitulos_totais(self) -> int:
        return self._capitulos_totais


    @property
    def capitulos_concluidos(self) -> int:
        return self._capitulos_concluidos


    @property
    def percentual_conclusao(self) -> float:
        """Calcula o percentual de conclusão da campanha com base nos capítulos."""

        return (self._capitulos_concluidos / self.capitulos_totais) * 100


    def avancar_capitulo(self, capitulos: int = 1) -> None:
        """Registra a conclusão de um ou mais capítulos da campanha. 
        
        Não avança uma quantidade de capítulos que ultrapasse o total de capítulos do Jogo

        Args:
            capitulos (int, optional): Número de capítulos a serem avançados. Padrão é 1.
        """

        # Registra o avanço de capítulos caso ele não exceda a quantidade de capítulos totais
        if (self._capitulos_concluidos + capitulos) <= self._capitulos_totais:
            self._capitulos_concluidos += capitulos
        # Caso o avanço ultrapasse o limite, ele apenas conclui o jogo inteiro
        else:
            self._capitulos_concluidos = self._capitulos_totais

    # Serialização para compatibilidade com JSON
    def to_dict(self):
        dados = super().to_dict()

        dados["capitulos_totais"] = self._capitulos_totais
        dados["capitulos_concluidos"] = self._capitulos_concluidos

        return dados

    # Desserialização a partir dos dados do JSON
    @classmethod
    def from_dict(cls, dados):
        jogo_campanha = JogoCampanha(dados["titulo"], dados["genero"], dados["plataforma"])
        jogo_campanha._status = dados["status"]
        jogo_campanha._horas_jogadas = dados["horas_jogadas"]
        jogo_campanha._avaliacao = dados["avaliacao"]
        jogo_campanha._data_inicio = dados["data_inicio"]
        jogo_campanha._data_termino = dados["data_termino"]
        jogo_campanha._id = dados["id"]
        jogo_campanha._capitulos_totais = dados["capitulos_totais"]
        jogo_campanha._capitulos_concluidos = dados["capitulos_concluidos"]

        return jogo_campanha


class JogoCompetitivo(Jogo):
    """Representa um jogo focado em partidas competitivas e rankings.

    Attributes:
        partidas_jogadas (int): Total de partidas disputadas.
        vitorias (int): Total de vitórias obtidas.
        derrotas (int): Total de derrotas sofridas.
        ranking_atual (str): Patamar atual no jogo (ex: 'Gold', 'Diamond').
    """

    def __init__(self, titulo: str, genero: str, plataforma: str) -> None:
        """Inicializa um jogo competitivo com estatísticas de partidas zeradas."""

        super().__init__(titulo, genero, plataforma)

        self._partidas_jogadas = 0
        self._vitorias = 0
        self._derrotas = 0
        self._ranking_atual = "Unranked"


    @property
    def partidas_jogadas(self) -> int:
        return self._partidas_jogadas


    @property
    def vitorias(self) -> int:
        return self._vitorias

    
    @property
    def derrotas(self) -> int:
        return self._derrotas

        raise PermissionError("Não é possível alterar o número de derrotas diretamente.")

    @property
    def ranking_atual(self) -> int:
        return self._ranking_atual

        raise PermissionError("Não é possível alterar o ranking atual diretamente.")
    
    @property
    def taxa_vitoria(self) -> float:
        """Calcula a porcentagem de vitórias em relação ao total de partidas."""

        return (self._vitorias / self._partidas_jogadas) * 100


    def registrar_partida(self, resultado: str) -> None:
        """Registra o resultado de uma nova partida jogada.

        Args:
            resultado (str): 'VITORIA' ou 'DERROTA'. É case-insensitive

        Raises:
            ValueError: Se o resultado informado for diferente de 'VITORIA' ou 'DERROTA'
        """

        resultadof = resultado.strip().upper()

        if resultadof == "VITORIA":
            self._vitorias += 1
            self._partidas_jogadas += 1
        elif resultadof == "DERROTA":
            self._derrotas += 1
            self._partidas_jogadas += 1
        else:
            raise ValueError("Resultado de partida inválido.")


    def atualizar_ranking(self, novo_ranking: str) -> None:
        """Atualiza a patente ou ranking atual do jogador.

        Args:
            novo_ranking (str): Nome do novo ranking/patente alcançado.

        Raises:
            ValueError: Se o novo ranking for igual ao atual
        """

        if novo_ranking != self._ranking_atual:
            self._ranking_atual = novo_ranking
        else:
            raise ValueError("O novo ranking não pode ser igual ao atual.")


    # Serialização para compatibilidade com JSON
    def to_dict(self):
        dados = super().to_dict()

        dados["partidas_jogadas"] = self._partidas_jogadas
        dados["vitorias"] = self._vitorias
        dados["derrotas"] = self._derrotas
        dados["ranking_atual"] = self._ranking_atual

        return dados

    # Desserialização a partir dos dados do JSON
    @classmethod
    def from_dict(cls, dados):
        jogo_competitivo = JogoCompetitivo(dados["titulo"], dados["genero"], dados["plataforma"])
        jogo_competitivo._status = dados["status"]
        jogo_competitivo._horas_jogadas = dados["horas_jogadas"]
        jogo_competitivo._avaliacao = dados["avaliacao"]
        jogo_competitivo._data_inicio = dados["data_inicio"]
        jogo_competitivo._data_termino = dados["data_termino"]
        jogo_competitivo._id = dados["id"]
        jogo_competitivo._partidas_jogadas = dados["partidas_jogadas"]
        jogo_competitivo._vitorias = dados["vitorias"]
        jogo_competitivo._derrotas = dados["derrotas"]
        jogo_competitivo._ranking_atual = dados["ranking_atual"]

        return jogo_competitivo
    

class JogoCooperativo(Jogo):
    """Representa um jogo com foco em sessões cooperativas e multiplayer local/online.

    Attributes:
        max_jogadores (int): Quantidade máxima de jogadores por sessão (>= 2)
        sessoes_coop (int): Total de sessões cooperativas realizadas.
        participantes_frequentes (list[str]): Lista de nomes dos parceiros frequentes de jogo.
    """

    def __init__(self, titulo: str, genero: str, plataforma: str, max_jogadores: int) -> None:
        """Inicializa um jogo cooperativo com 0 sessões realizadas e lista de parceiros vazia"""

        super().__init__(titulo, genero, plataforma)

        if max_jogadores < 2:
            raise ValueError("O jogo deve suportar ao menos 2 jogadores por sessão")
        else:
            self._max_jogadores = max_jogadores

        self._sessoes_coop = 0
        self._participantes_frequentes = []


    @property
    def max_jogadores(self) -> int:
        return self._max_jogadores


    @property
    def sessoes_coop(self) -> int:
        return self._sessoes_coop


    def adicionar_participante(self, nome: str) -> None:
        """Adiciona o nome de um parceiro de jogatina à lista de frequentes.

        Args:
            nome (str): Nome ou nickname do jogador parceiro.

        Raises:
            ValueError: Se o nome do parceiro for vazio.
        """

        if nome != "":
            self._participantes_frequentes.append(nome.strip())
        else:
            raise ValueError("O nome do participante não pode ser vazio")


    def registrar_sessao(self) -> None:
        """Incrementa o número de sessões coop concluídas em uma unidade"""

        self._sessoes_coop += 1


    # Serialização para compatibilidade com JSON
    def to_dict(self):
        dados = super().to_dict()

        dados["max_jogadores"] = self._max_jogadores
        dados["sessoes_coop"] = self._sessoes_coop
        dados["participantes_frequentes"] = self._participantes_frequentes

        return dados

    # Desserialização a partir dos dados do JSON
    @classmethod
    def from_dict(cls, dados):
        jogo_cooperativo = JogoCooperativo(dados["titulo"], dados["genero"], dados["plataforma"], dados["max_jogadores"])
        jogo_cooperativo._status = dados["status"]
        jogo_cooperativo._horas_jogadas = dados["horas_jogadas"]
        jogo_cooperativo._avaliacao = dados["avaliacao"]
        jogo_cooperativo._data_inicio = dados["data_inicio"]
        jogo_cooperativo._data_termino = dados["data_termino"]
        jogo_cooperativo._id = dados["id"]
        jogo_cooperativo._sessoes_coop = dados["sessoes_coop"]
        jogo_cooperativo._participantes_frequentes = dados["participantes_frequentes"]

        return jogo_cooperativo