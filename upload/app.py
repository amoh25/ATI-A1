from flask import *
from flask_sqlalchemy import SQLAlchemy
import requests
import os
from dotenv import load_dotenv

load_dotenv()

URI=os.getenv('URI')
auth=False

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = URI
app.config['AUTH'] = False
db = SQLAlchemy(app)


class Upload(db.Model):
    __tablename__ = 'upload'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    path = db.Column(db.String(200))

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        payload = {'username': username, 'password': password}
        res = requests.post('http://127.0.0.1:5000', data=payload)
        if res.status_code == 200:
            app.config['AUTH'] = True
            return redirect(url_for('upload_file'))
        else:
            app.config['AUTH'] = False
            return redirect(url_for('login'))

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        if app.config['AUTH']:
            return render_template('upload.html')
        else:
            return redirect(url_for('login'))
    if request.method == 'POST':
        file = request.files['file']
        name = file.filename
        if not os.path.exists('videos'):
            os.mkdir('videos')
        path = os.path.abspath(f'videos/{name}')
        save = file.save(path)
        upload = Upload(name=name, path=path)
        db.session.add(upload)
        db.session.commit()
        return redirect(f'http://127.0.0.1:5100/videos')


if __name__=='__main__':
    app.run(port=5050,debug=True)