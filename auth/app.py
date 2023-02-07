from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

URI=os.getenv('URI')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = URI
db = SQLAlchemy(app)


class Users(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(300),nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

with app.app_context():
    db.create_all()
    if db.session.query(Users).first() == None:
        for i in range(7):
            user = Users(f'user{i}', 'password')
            db.session.add(user)
            db.session.commit()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
    return is_user(username, password)


def is_user(username, password):
        try:
            user = db.session.query(Users).filter_by(username=username).one()
        except:
            return 'Invalid Login', 401
        if user.check_password(password):
            return '', 200
        else:
            return 'Invalid Login', 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)