from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:garbage@localhost:8889/build-a-blog'
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


@app.route('/blog')
def blog():
    entries = Blog.query.all()
    return render_template('entries.html', entries=entries)

@app.route('/newpost')
def newpostcreation():
        return render_template('new-entry.html')
@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    if request.method == 'POST':
        entry_title = request.form['title']
        entry_post = request.form['entry']
        new_entry = Blog(entry_title, entry_post, None)
        db.session.add(new_entry)
        db.session.commit()
    return redirect('/blog')






if __name__ == '__main__':
    app.run()