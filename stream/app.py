from flask import *
from flask_sqlalchemy import SQLAlchemy
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
    path = db.Column(db.String(200))

@app.route('/view/<id>')
def view(id):
    upload = db.session.query(Upload).filter_by(id=id).one()
    if not upload:
        return 'File not found', 404
    send = send_file(upload.path, mimetype='video/mp4')
    return send

if __name__=='__main__':
    app.run(port=5100,debug=True)