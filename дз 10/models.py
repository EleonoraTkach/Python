
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String,Integer,Identity

class Base(DeclarativeBase):
	pass

class Student(Base):
	__tablename__ = "student"

	id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
	last_name: Mapped[str] = mapped_column(String(50))
	first_name: Mapped[str] = mapped_column(String(50))
	faculty: Mapped[str] = mapped_column(String(50))
	course: Mapped[str] = mapped_column(String(50))
	grade: Mapped[int] = mapped_column(Integer)

	def __str__(self) -> str:
		return (f"Студент: {self.last_name} {self.first_name}\n"
				f"Факультет: {self.faculty}\n"
				f"Курс: {self.course}\n"
				f"Оценка: {self.grade}\n"
				f"ID: {self.id}")

	def to_dict(self):
		return {
			"id": self.id,
			"last_name": self.last_name,
			"first_name": self.first_name,
			"faculty": self.faculty,
			"course": self.course,
			"grade": self.grade
		}