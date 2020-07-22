class AI(Player):
    def __init__(self, client_number, name="Gator", ai_bot_bool=True):
        super().__init__(client_number, name, ai_bot_bool)
        self._ehs = None
        self._hs = None
        self._npot = None
        self._ppot = None

    @property
    def ehs(self):
        return self._ehs

    @property
    def hs(self):
        return self._hs

    @property
    def npot(self):
        return self._npot

    @property
    def ppot(self):
        return self._ppot

    @ehs.setter
    def ehs(self, ehs):
        self._ehs = ehs

    @hs.setter
    def hs(self, hs):
        self._hs = hs

    @npot.setter
    def npot(self, npot):
        self._npot = npot

    @ppot.setter
    def ppot(self, ppot):
        self._ppot = ppot

    
