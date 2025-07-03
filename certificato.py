
class Certificato():
    def __init__(self, reparto, nome, localita, provincia, paese, email):
        self._reparto = reparto
        self._nome = nome
        self._localita = localita
        self._provincia = provincia
        self._paese = paese
        self._email = email
    
    @property
    def reparto(self):
        return self._reparto
    
    @reparto.setter
    def reparto(self, testo):
        if testo == (""):
            raise ValueError("Inserire un reparto")
        self._reparto = testo
    
    @property
    def nome(self):
        return self._nome
    
    @nome.setter
    def nome(self, testo):
        if testo == (""):
            raise ValueError("Inserire un nome account")
        self._nome = testo
    
    @property
    def localita(self):
        return self._localita
    
    @localita.setter
    def localita(self, testo):
        if testo == (""):
            raise ValueError("Inserire una località")
        self._localita = testo

    @property
    def provincia(self):
        return self._provincia
    
    @provincia.setter
    def provincia(self, testo):
        if testo == (""):
            raise ValueError("Inserire una provincia")
        self._provincia = testo

    @property
    def paese(self):
        return self._paese
    
    @paese.setter
    def paese(self, testo):
        if testo == (""):
            raise ValueError("Inserire un paese")
        self._paese = testo

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, testo):
        if testo == (""):
            raise ValueError("Inserire una email")
        self._email = testo
