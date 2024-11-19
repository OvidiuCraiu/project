FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Initialize the database
RUN python init_db.py

CMD ["python", "run.py"]

RUN pip install --upgrade pip
RUN pip install flask-sqlalchemy
RUN pip install "SQLAlchemy<2.0"
