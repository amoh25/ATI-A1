from flask import *
from flask_sqlalchemy import SQLAlchemy
import io
import requests
import os
from dotenv import load_dotenv

load_dotenv()

URI=os.getenv('URI')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = URI
db = SQLAlchemy(app)

class Upload(db.Model):
    __tablename__ = 'upload'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    data = db.Column(db.LargeBinary(4294967295))

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
            return redirect(url_for('upload_file'))
        else:
            return redirect(url_for('login'))

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('upload.html')
    if request.method == 'POST':
        file = request.files['file']
        name = file.filename
        data = file.read()
        upload = Upload(name=name, data=data)
        db.session.add(upload)
        db.session.commit()
        return redirect(url_for('upload'))

@app.route('/get/<id>')
def get(id):
    upload = Upload.query.get(id)
    send = send_file(io.BytesIO(upload.data), attachment_filename=upload.name)
    return send

@app.route('/get/<id>/view')
def view(id):
    upload = Upload.query.get(id)
    return Response(upload.data, content_type='video/mp4')


if __name__=='__main__':
    app.run(port=5050,debug=True)