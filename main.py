from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:beproductive@localhost:8889/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'VF%^ghyjGRSfs4545&^FGS^5$%'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    entry = db.Column(db.Text)
    date = db.Column(db.DateTime)

    def __init__(self, title, entry, date):
        self.title = title
        self.entry = entry
        if date is None:
            date = datetime.utcnow()
        self.date = date

@app.route('/')
def index():
    return "No snoop plz"


@app.route('/blog', methods=['POST'])
def blog():
    return render_template('entries.html')





if __name__ == '__main__':
    app.run()