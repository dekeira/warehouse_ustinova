import mysql.connector

class DBManager:
    def __init__(self, host='localhost', user='root', password='root', database='warehouse'):
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }

    def get_connection(self):
        return mysql.connector.connect(**self.config)

    def get_free_slots(self):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT SUM(s.kolichestvo_yacheek) - COUNT(p.id) as free_slots
                    FROM Stelezhka s
                    LEFT JOIN Pozitsiya p ON s.Kod_stelezhki = p.Kod_stelezhki
                """)
                res = cursor.fetchone()
                return res['free_slots'] or 0
        except Exception as e:
            logging.error("Ошибка при получении свободных ячеек", exc_info=True)
            raise

    def get_rack_stats(self):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT 
                        s.nomer as stel_nomer,
                        ROUND((COUNT(p.id) * 100.0 / s.kolichestvo_yacheek), 2) as fill_percent,
                        s.dopustimaya_massa
                    FROM Stelezhka s
                    LEFT JOIN Pozitsiya p ON s.Kod_stelezhki = p.Kod_stelezhki
                    GROUP BY s.Kod_stelezhki
                    ORDER BY s.nomer
                """)
                rows = cursor.fetchall()
                return [
                    (row['stel_nomer'], row['fill_percent'], row['dopustimaya_massa'])
                    for row in rows
                ]
        except Exception as e:
            logging.error("Ошибка при получении статистики по стеллажам", exc_info=True)
            raise

# Тестовые наборы и тестирование модуля DB запускать этот файл для тестирования
if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.DEBUG)

    db = DBManager(
        host='localhost',
        user='root',
        password='root',
        database='warehouse'
    )

    print("Отладка подключения и запросов")
    try:
        free = db.get_free_slots()
        print("Свободных ячеек:", free)

        stats = db.get_rack_stats()
        print("Статистика стеллажей:")
        for num, fill, weight in stats:
            print(f"  Стеллаж {num}: {fill}% заполнен, макс. {weight} кг")
    except Exception as e:
        print("Ошибка:", e)
        logging.exception("Подробности:")