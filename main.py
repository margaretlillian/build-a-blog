from datetime import datetime
from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

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

    def __repr__(self):
        return str(self.id)

@app.route('/')
def index():
    return "No snoop plz"


@app.route('/blog')
def blog():
    entries = Blog.query.all()
    post_id = request.args.get('id')
    entry = Blog.query.filter_by(id=post_id).first()
    if not post_id:
        return render_template('entries.html', entries=entries)
    else:
        return render_template('entry.html', entry=entry)

@app.route('/newpost')
def newpostnotyetcreated():
        return render_template('new-entry.html')

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    if request.method == 'POST':
        entry_title = request.form['title']
        entry_post = request.form['entry']
        new_entry = Blog(entry_title, entry_post, None)
        db.session.add(new_entry)
        db.session.commit()
    new_post = Blog.query.get(new_entry.id)
    return redirect('/blog?id={0}'.format(new_post))


if __name__ == '__main__':
    app.run()