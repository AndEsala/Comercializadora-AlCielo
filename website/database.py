from flask_sqlalchemy import SQLAlchemy

# Create a new SQLAlchemy object
db = SQLAlchemy()

# Initialize the database
def init_db(app):
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        db.session.commit()