FROM python:3.11@sha256:44729cbb05832da5c0c1c6481814e71e20731933a32b3401ee510f79e8185d4b

WORKDIR /app

COPY ./backend/python_app /app
COPY ./backend/python_app/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py", "-d", "1"]
