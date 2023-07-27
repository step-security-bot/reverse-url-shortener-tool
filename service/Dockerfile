FROM python:3.11

WORKDIR /app

COPY ./backend/python_app /app
COPY ./backend/python_app/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py", "-d", "1"]
