"""Módulo contendo classe principal de jogo para uma experiência genérica de jogatina"""

class Jogo:
    """Representa a classe base de um jogo no catálogo.

    Armazena e gerencia os dados fundamentais de um jogo, como título,
    gênero, plataforma, status de conclusão e horas jogadas.

    Attributes:
        titulo (str): Título principal do jogo.
        genero (str): Gênero do jogo (ex: 'RPG', 'Ação', 'Estratégia').
        plataforma (str): Plataforma em que é jogado (ex: 'PC', 'Console', 'Mobile').
        status (str): Estado atual do jogo ('NÃO INICIADO', 'JOGANDO', 'FINALIZADO').
        horas_jogadas (float): Total de horas acumuladas de jogatina (deve ser >= 0).
        avaliacao (float): Nota do jogo de 0 a 10 (atribuível apenas quando finalizado).
    """

    def __init__(self, titulo: str, genero: str, plataforma: str) -> None:
        """Inicializa um novo jogo com status 'NÃO INICIADO' e zero horas jogadas."""
        self._titulo = None
        self.genero = genero
        self.plataforma = plataforma
        self.status = "NÃO INICIADO"
        self._horas_jogadas = 0
        self._avaliacao = None

        # Irá ativar o setter de "titulo" logo na inicialização da classe
        self.titulo = titulo

    @property
    def titulo(self) -> str:
        return self._titulo

    @titulo.setter
    def titulo(self, novo_titulo: str) -> None:
        """Define um novo título para o jogo caso este não seja uma string vazia"""

        if novo_titulo == "":
            raise NameError("Não é possível criar um jogo com nome vazio")
        else:
            self._titulo = novo_titulo.strip()

    @property
    def avaliacao(self) -> float:
        return self._avaliacao

    @avaliacao.setter
    def avaliacao(self, nota: float) -> None:
        """Define uma nota de avaliação para o jogo caso ele esteja com o status 'FINALIZADO' e valor esteja entre 0 e 10"""

        if self.status != "FINALIZADO": 
            raise PermissionError("Só é possível avaliar um jogo quando ele for FINALIZADO.")
        else:
            if not (0 <= nota <= 10): 
                raise ValueError("Só são permitidas notas no intervalo de zero a dez.")
            else: # Se estiver no intervalo correto, ele atribui
                self._avaliacao = nota

    @property
    def horas_jogadas(self) -> float:
        return self._horas_jogadas

    @horas_jogadas.setter
    def horas_jogadas(self, horas: float) -> None:
        """Muda a quantidade de horas jogadas de forma compulsória. Mas é útil em métodos como 'reiniciar_jogo'
        
        Args:
            horas (float): Quantidade de horas jogadas

        Raises:
            ValueError: Se fornecida uma quantidade de horas abaixo de zero
        """

        if horas < 0:
            raise ValueError("Não é permitido configurar as horas jogadas para valores abaixo de zero")
        else:
            self._horas_jogadas = horas

    def __repr__(self) -> str:
        """Retorna uma mensagem técnica para o desenvolvedor com fins de depuração"""
        return (
        f"Jogo("
        f"titulo={self._titulo!r}, "
        f"genero={self.genero!r}, "
        f"plataforma={self.plataforma!r}, "
        f"status={self.status!r}, "
        f"horas_jogadas={self._horas_jogadas!r}, "
        f"avaliacao={self._avaliacao!r}"
        f")"
    )

    def __str__(self) -> str:
        """Retorna um resumo amigável e formatado do jogo em formato de card."""

        icones_status = {
            "NÃO INICIADO": "⏳ [Não Iniciado]",
            "JOGANDO": "🎮 [Jogando]",
            "FINALIZADO": "🏆 [Finalizado]"
        }
        
        statusf = icones_status.get(self.status, self.status) # O segundo argumento repetido é um fallback caso não haja chave correspondente
        notaf = f"{self._avaliacao:.1f}/10" if self._avaliacao is not None else "Sem nota"

        comprimento_titulo = len(f"────────── 🕹️ {self._titulo.upper()} ──────────")
        resumo = (
            f"\n┌────────── 🕹️  {self._titulo.upper()} ──────────┐\n\n"
            f"   📂 Gênero: {self.genero}\n"
            f"   💻 Plataforma: {self.plataforma}\n"
            f"   ⏱️  Horas Jogadas: {self._horas_jogadas:.1f}\n"
            f"   ⭐ Avaliação: {notaf}\n"
            f"   📌 Status: {statusf}\n\n"
            f"└{comprimento_titulo * '─'}┘"
        )
    
        return resumo

    def __eq__(self, outro_jogo: Jogo) -> bool:
        """Verifica se um jogo é igual a outro com base no título e na plataforma de ambos"""

        if self._titulo == outro_jogo._titulo and self.plataforma == outro_jogo.plataforma:
            return True
        else:
            return False

    def __lt__(self, outro_jogo: Jogo) -> bool:
        """Verifica se um jogo tem menos horas jogadas em relação a outro"""

        return self._horas_jogadas < outro_jogo._horas_jogadas

    def registrar_progresso(self, horas: float) -> None:
        """Incrementa as horas jogadas e atualiza o status do jogo.

        Args:
            horas (float): Quantidade de horas adicionadas na sessão.

        Raises:
            ValueError: Se a quantidade de horas for menor ou igual a zero.
        """

        if horas > 0:
            self._horas_jogadas += horas
            if self.status != "JOGANDO":
                self.status = "JOGANDO"
        else:
            raise ValueError("Horas negativas não são incrementadas")

    def finalizar_jogo(self) -> None:
        """Marca o jogo como 'FINALIZADO' caso ele tenha pelo menos uma hora de jogatina

        Raises:
            PermissionError: Se o jogo tiver menos de 1 hora jogada
        """

        if self._horas_jogadas < 1:
            raise PermissionError("Só é possível finalizar um jogo depois de pelo menos 1 hora de jogatina.")
        else:
            self.status = "FINALIZADO"

    def avaliar_jogo(self, nota: float) -> None:
        """Atribui uma nota ao jogo depois de finalizado
        
        Args:
            nota (float): Nota que deve estar entre 0 e 10
        """

        self.avaliacao = nota # Irá invocar o setter de avaliação
