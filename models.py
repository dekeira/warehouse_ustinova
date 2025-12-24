class Stelezhka:
    def __init__(self, kod_stelezhki: int, nomer: int, kolichestvo_yacheek: int, dopustimaya_massa: float):
        self.kod_stelezhki = kod_stelezhki
        self.nomer = nomer
        self.kolichestvo_yacheek = kolichestvo_yacheek
        self.dopustimaya_massa = dopustimaya_massa


class Gruz:
    def __init__(self, kod_gruza: int, nazvanie: str):
        self.kod_gruza = kod_gruza
        self.nazvanie = nazvanie


class Pozitsiya:
    def __init__(self, id: int, kod_gruza: int, kod_stelezhki: int, nomer_yacheiki: int, massa: float, data_ukladki: str):
        self.id = id
        self.kod_gruza = kod_gruza
        self.kod_stelezhki = kod_stelezhki
        self.nomer_yacheiki = nomer_yacheiki
        self.massa = massa
        self.data_ukladki = data_ukladki