from app import create_app, init_db

app = create_app()
with app.app_context():
    db.create_all()
    print("Database tables created.")
