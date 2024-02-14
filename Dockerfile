# Docker-команда FROM вказує базовий образ контейнера
FROM python:3.10.5-slim-buster

# Встановимо робочу директорію усередині контейнера
WORKDIR .

# Якщо не змінювались то не завантажує
COPY ./requirements.txt .

# Встановимо залежності усередині контейнера
RUN pip install -r requirements.txt  # pip freeze > requirements.txt

# Копіюємо main.py та директорію src до /app

COPY . .

# Позначимо порт де працює програма всередині контейнера
EXPOSE 8000


# Запустимо нашу програму всередині контейнера
CMD ["python", "app.py"]