import pymysql
from pymysql.cursors import DictCursor
from models import Stelezhka
from models import Gruz
from models import Pozitsiya

class DBManager:
    def __init__(self, host='localhost', user='root', password='root', database='warehouse'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def get_connection(self):
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            cursorclass=DictCursor
        )

    def load_stelezhki(self):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT Kod_stelezhki, nomer, kolichestvo_yacheek, dopustimaya_massa FROM Stelezhka")
                return [Stelezhka(r['Kod_stelezhki'], r['nomer'], r['kolichestvo_yacheek'], r['dopustimaya_massa']) for r in cur.fetchall()]

    def load_gruzy(self):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT Kod_gruza, nazvanie FROM Gruz")
                return [Gruz(r['Kod_gruza'], r['nazvanie']) for r in cur.fetchall()]

    def load_pozitsii(self):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, Kod_gruza, Kod_stelezhki, nomer_yacheiki, massa, data_ukladki FROM Pozitsiya")
                return [
                    Pozitsiya(
                        r['id'], r['Kod_gruza'], r['Kod_stelezhki'],
                        r['nomer_yacheiki'], r['massa'], r['data_ukladki']
                    ) for r in cur.fetchall()
                ]

# === ТЕСТОВЫЙ ЗАПУСК (как в примере) ===
if __name__ == '__main__':
    db = DBManager()
    print("Тест загрузки данных из БД:")
    try:
        stel = db.load_stelezhki()
        gruz = db.load_gruzy()
        poz = db.load_pozitsii()
        print(f"Стеллажей: {len(stel)}, Грузов: {len(gruz)}, Позиций: {len(poz)}")
        if stel:
            print(f"Пример стеллажа: №{stel[0].nomer}, ячеек: {stel[0].kolichestvo_yacheek}")
        if poz:
            print(f"Пример позиции: ячейка {poz[0].nomer_yacheiki}, масса {poz[0].massa} кг")
    except Exception as e:
        print("Ошибка:", e)