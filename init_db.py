from app import create_app, init_db

app = create_app()
init_db(app)

RUN pip install --upgrade pip
RUN pip install flask-sqlalchemy
RUN pip install "SQLAlchemy<2.0"
