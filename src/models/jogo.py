"""Módulo contendo classe principal Jogo para gerenciar uma experiência genérica de jogatina"""

from datetime import date, datetime

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
        data_inicio (date): Data que o jogo foi jogado pela primeira vez.
        data_termino (date): Data que o jogo foi finalizado.
    """

    def __init__(self, titulo: str, genero: str, plataforma: str) -> None:
        """Inicializa um novo jogo com status 'NÃO INICIADO' e zero horas jogadas."""
        self._titulo = None
        self._genero = genero
        self._plataforma = plataforma
        self._status = "NÃO INICIADO"
        self._horas_jogadas = 0
        self._avaliacao = None
        self._data_inicio = None
        self._data_termino = None
        self._id = None

        # Irá ativar o setter de "titulo" logo na inicialização da classe
        self.titulo = titulo


    @property
    def titulo(self) -> str:
        return self._titulo


    @titulo.setter
    def titulo(self, novo_titulo: str) -> None:
        """Define um novo título para o jogo caso não seja uma string vazia"""

        if novo_titulo == "":
            raise NameError("Não é possível criar um jogo com nome vazio")
        else:
            self._titulo = novo_titulo.strip()


    @property
    def avaliacao(self) -> float:
        return self._avaliacao


    @avaliacao.setter
    def avaliacao(self, nota: float) -> None:
        """Define uma nota para o jogo caso esteja com status 'FINALIZADO' e o valor esteja entre 0 e 10"""

        if self._status != "FINALIZADO": 
            raise PermissionError("Só é possível avaliar um jogo quando ele for FINALIZADO.")
        else:
            if not (0 <= nota <= 10): 
                raise ValueError("Só são permitidas notas no intervalo de zero a dez.")
            else: # Se estiver no intervalo correto, ele atribui
                self._avaliacao = nota


    @property
    def horas_jogadas(self) -> float:
        return self._horas_jogadas


    @property
    def data_inicio(self) -> str:
        """Retorna a data de início do jogo formatada no padrão brasileiro
        
        Raises:
            AttributeError: caso o jogo ainda não tenha sido iniciado
        """
        if self._data_inicio is not None:
            dataf = self._data_inicio.strftime("%d/%m/%Y")
            return dataf
        else:
            raise AttributeError("O jogo ainda não foi iniciado, logo não possui data de início.")


    @property
    def data_termino(self) -> str:
        """Retorna a data de término do jogo formatada no padrão brasileiro

        Raises:
            AttributeError: caso o jogo ainda não tenha sido finalizado
        """
        if self._data_termino is not None:
            dataf = self._data_termino.strftime("%d/%m/%Y")
            return dataf
        else:
            raise AttributeError("O jogo ainda não foi finalizado, logo não possui data de término.")


    def __repr__(self) -> str:
        """Retorna uma mensagem técnica para o desenvolvedor com fins de depuração"""
        return (
        f"Jogo("
        f"titulo={self._titulo!r}, "
        f"genero={self._genero!r}, "
        f"plataforma={self._plataforma!r}, "
        f"status={self._status!r}, "
        f"horas_jogadas={self._horas_jogadas!r}, "
        f"avaliacao={self._avaliacao!r}, "
        f"data_inicio={self._data_inicio!r}, "
        f"data_termino={self._data_termino!r},"
        f"id={self._id!r}"
        f")"
    )


    def __str__(self) -> str:
        """Retorna um resumo amigável e formatado do jogo em formato de card."""

        icones_status = {
            "NÃO INICIADO": "[Não Iniciado]",
            "JOGANDO": "[Jogando]",
            "FINALIZADO": "[Finalizado]"
        }

        # Formatação de alguns atributos para facilitar os prints:
        statusf = icones_status.get(self._status, self._status) # O segundo argumento repetido é um fallback, caso não haja chave correspondente aí ele retorna o próprio argumento
        notaf = f"{self._avaliacao:.1f}/10" if self._avaliacao is not None else "Sem nota"
        data_iniciof = self.data_inicio if self._data_inicio is not None else ""
        data_terminof = self.data_termino if self._data_termino is not None else ""

        comprimento_titulo = len(f"────────── 🕹️ {self._titulo.upper()} ──────────")
        resumo = (
            f"\n┌────────── 🕹️  {self._titulo.upper()} ──────────┐\n\n"
            f"  📂 Gênero: {self._genero}\n"
            f"  💻 Plataforma: {self._plataforma}\n"
            f"  ⏱️  Horas Jogadas: {self._horas_jogadas:.1f}\n"
            f"  ⭐ Avaliação: {notaf}\n"
            f"  📌 Status: {statusf}\n"
            f"  📆 Data de Início: {data_iniciof}\n"
            f"  🗓️  Data de Término: {data_terminof}\n\n"
            f"└{comprimento_titulo * '─'}┘"
        )
    
        return resumo


    def __eq__(self, outro_jogo: Jogo) -> bool:
        """Verifica se um jogo é igual a outro com base no título e na plataforma de ambos"""

        if self._titulo == outro_jogo._titulo and self._plataforma == outro_jogo._plataforma:
            return True
        else:
            return False


    def __lt__(self, outro_jogo: Jogo) -> bool:
        """Verifica se um jogo tem menos horas jogadas em relação a outro"""

        return self._horas_jogadas < outro_jogo._horas_jogadas


    def registrar_progresso(self, horas: float) -> None:
        """Incrementa as horas jogadas e atualiza o status do jogo.

        Também define a data de início do jogo caso seja a primeira gameplay
        
        Args:
            horas (float): Quantidade de horas adicionadas na sessão.

        Raises:
            ValueError: Se a quantidade de horas for menor ou igual a zero.
        """

        if horas > 0:
            if self._horas_jogadas == 0:
                self._data_inicio = date.today()
            self._horas_jogadas += horas
            if self._status != "JOGANDO":
                self._status = "JOGANDO"
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
            self._status = "FINALIZADO"
            self._data_termino = date.today()


    def reiniciar_jogo(self) -> None:
        """Marca o jogo como 'JOGANDO', anula as horas jogadas e redefine as datas de início e de término"""
        self._status = "JOGANDO"
        self._horas_jogadas = 0
        self._data_inicio = date.today()
        self._data_termino = None


    def avaliar_jogo(self, nota: float) -> None:
        """Atribui uma nota ao jogo depois de finalizado"""

        self.avaliacao = nota # Não precisa de validação, pois invoca o setter


    # Serialização para compatibilidade com JSON
    def to_dict(self):
        return{
            "titulo": self._titulo,
            "genero": self._genero,
            "plataforma": self._plataforma,
            "status": self._status,
            "horas_jogadas": self._horas_jogadas,
            "avaliacao": self._avaliacao,
            # Não podemos guardar objetos date dentro do JSON, para isso chamei o getter que retorna uma string
            "data_inicio": self.data_inicio if self._data_inicio != None else None,
            "data_termino": self.data_termino if self._data_termino != None else None,
            "id": self._id
        }

    # Desserialização a partir dos dados do JSON
    @classmethod
    def from_dict(cls, dados: dict):
        jogo = Jogo(dados["titulo"], dados["genero"], dados["plataforma"])
        jogo._status = dados["status"]
        jogo._horas_jogadas = dados["horas_jogadas"]
        jogo._avaliacao = dados["avaliacao"]

        
        if dados["data_inicio"] != None:
            # Interpreta data em string e transforma em objeto date
            jogo._data_inicio = datetime.strptime(dados["data_inicio"], "%d/%m/%Y").date()
        else:
            jogo._data_inicio = None

        if dados["data_termino"] != None:
            # Interpreta data em string e transforma em objeto date
            jogo._data_termino = datetime.strptime(dados["data_termino"], "%d/%m/%Y").date()
        else:
            jogo._data_termino = None

        jogo._id = dados["id"]

        return jogo