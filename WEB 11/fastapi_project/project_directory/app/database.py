# database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import SQLALCHEMY_DATABASE_URL  # Імпортуємо змінну підключення з файлу config.py

# Створюємо об'єкт для з'єднання з базою даних
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Створюємо базовий клас для всіх моделей
Base = declarative_base()

# Створюємо функцію для отримання сесії з бази даних
def get_db():
    db = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return db()
