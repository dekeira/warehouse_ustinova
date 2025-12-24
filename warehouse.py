from db import DBManager
from models import Stelezhka
from models import Gruz
from models import Pozitsiya

class Warehouse:
    def __init__(self):
        self.db = DBManager()
        self.stelezhki: list[Stelezhka] = []
        self.gruzy: list[Gruz] = []
        self.pozitsii: list[Pozitsiya] = []

    def load_all(self):
        self.stelezhki = self.db.load_stelezhki()
        self.gruzy = self.db.load_gruzy()
        self.pozitsii = self.db.load_pozitsii()

    def get_free_slots(self) -> int:
        total = sum(s.kolichestvo_yacheek for s in self.stelezhki)
        occupied = len(self.pozitsii)
        return total - occupied

    def get_rack_stats(self) -> list[tuple[int, float, float]]:
        # карта стеллажей по id
        stel_map = {s.kod_stelezhki: s for s in self.stelezhki}
        # считаем занятые ячейки по стеллажам
        occupied_by_rack = {}
        for p in self.pozitsii:
            occupied_by_rack[p.kod_stelezhki] = occupied_by_rack.get(p.kod_stelezhki, 0) + 1

        result = []
        for s in sorted(self.stelezhki, key=lambda x: x.nomer):
            occ = occupied_by_rack.get(s.kod_stelezhki, 0)
            fill_pct = round(occ / s.kolichestvo_yacheek * 100, 2)
            result.append((s.nomer, fill_pct, s.dopustimaya_massa))
        return result