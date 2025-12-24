from warehouse import Warehouse


def main():
    print("=== Склад: отчёт по стеллажам ===\n")

    try:
        warehouse = Warehouse()
        print("Загрузка данных из базы...")
        warehouse.load_all()
        print("✓ Загружено\n")

        free = warehouse.get_free_slots()
        print(f"🔹 Свободных ячеек: {free}\n")

        print("🔹 Заполнение стеллажей:")
        stats = warehouse.get_rack_stats()
        if not stats:
            print("  — Нет данных")
        else:
            for num, fill, weight in stats:
                print(f"  Стеллаж №{num}: {fill:5.1f}% | макс. {weight} кг")

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()