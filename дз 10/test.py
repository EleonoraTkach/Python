from DataBase import DataBase
from models import Student


def test_database_with_student_table():
    """Тест базы данных с таблицей student"""
    print("=== ТЕСТ БАЗЫ ДАННЫХ ===")

    # Используем базу в памяти
    db = DataBase('sqlite:///:memory:')

    print("1. Создаем базу и таблицы...")
    db.create_db_and_tables()

    print("2. Создаем студента...")
    student = Student(
        first_name="Иван",
        last_name="Петров",
        faculty="Информатика",
        course=2,
        grade=4.5
    )

    try:
        created_student = db.create_student(student)
        print(f"   ✅ Студент создан с ID: {created_student.id}")

        # Пробуем получить студента
        retrieved = db.get_student_by_id(created_student.id)
        if retrieved:
            print(f"   ✅ Студент получен: {retrieved.first_name} {retrieved.last_name}")
        else:
            print("   ❌ Не удалось получить студента")

    except Exception as e:
        print(f"   ❌ Ошибка: {e}")


if __name__ == "__main__":
    test_database_with_student_table()