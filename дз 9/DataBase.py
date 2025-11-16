from typing import List, Tuple
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from models import Student, Base


class DataBase:
    def __init__(self, db_url: str = None):
        if db_url is None:
            db_url = 'sqlite:///students.db'

        self.engine = create_engine(db_url, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def create_db_and_tables(self) -> None:
        try:
            Base.metadata.create_all(self.engine)
            print("База данных и таблицы успешно созданы!")
        except Exception as e:
            print(f"Ошибка при создании базы данных: {e}")

    @contextmanager
    def get_session(self):
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def create_student(self, student: Student) -> None:
        with self.get_session() as session:
            session.add(student)


    def get_by_faculty(self, faculty: str) -> List[Student]:
        with self.get_session() as session:
            statement = select(Student).where(Student.faculty == faculty)
            return session.scalars(statement).all()

    def get_unic_course(self) -> List[str]:
        with self.get_session() as session:
            statement = select(Student.course).distinct()
            return session.scalars(statement).all()

    def get_facult_grade_avg(self) -> List[Tuple[str, float]]:
        with self.get_session() as session:
            statement = select(
                Student.faculty,
                func.avg(Student.grade).label('avg_grade')
            ).group_by(Student.faculty)

            result = session.execute(statement).all()
            return [(row.faculty, float(row.avg_grade)) for row in result]

    def close_connection(self) -> None:
        self.engine.dispose()