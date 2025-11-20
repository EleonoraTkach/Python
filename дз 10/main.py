from models import Student
from DataBase import DataBase
import csv

csv_file_path = 'C:\\Users\\eleon\\Downloads\\students.csv'

try:
    students = []
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:

            student = Student(
                first_name=row['Фамилия'],
                last_name=row['Имя'],
                faculty=(row['Факультет']),
                course=row.get('Курс'),
                grade = int(row.get('Оценка'))
            )
            students.append(student)

    db = DataBase()
    db.create_db_and_tables()
    for i in students:
        db.create_student(i)

    print(f"Успешно добавлено {len(students)} студентов в базу")



except Exception as e:
    print(f"Ошибка: {e}")