from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

class NewUsers(db.Model):
    __tablename__ = 'new_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    folder_path = db.Column(db.String(255), nullable=False)
    image1 = db.Column(db.LargeBinary, nullable=False)
    image2 = db.Column(db.LargeBinary, nullable=False)
    image3 = db.Column(db.LargeBinary, nullable=False)
    image1_filename = db.Column(db.String(255), nullable=False)
    image2_filename = db.Column(db.String(255), nullable=False)
    image3_filename = db.Column(db.String(255), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class security_db(db.Model):
    __tablename__ = 'ai_security_images'
    id = db.Column(db.Integer, primary_key=True)
    image_data = db.Column(db.LargeBinary)
    timestamp = db.Column(db.DateTime)

def create_user(username, password):
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return user

if __name__ == '__main__':
    from werkzeug.security import generate_password_hash
    with app.app_context():
        inspector = inspect(db.engine)
        if not inspector.has_table('new_users'):
            db.create_all()
            print("Database table created successfully!")
        else:
            print("Database table already exists!")
        # create_user('admin', 'your_password')
        
        username = 'admin'
        password = 'project'
        existing_user = db.session.query(User).filter_by(username=username).first()
        if existing_user:
            print("User already exists")
        else:
            password = generate_password_hash(password)
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            print("User created successfully")
 