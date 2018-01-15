from datetime import datetime
from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:garbage@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'VF%^ghyjGRSfs4545&^FGS^5$%'

class Post(db.Model):

    entry_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    entry = db.Column(db.Text)
    date = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __init__(self, title, entry, date, category):
        self.title = title
        self.entry = entry
        if date is None:
            date = datetime.utcnow()
        self.date = date
        self.category = category

    def __repr__(self):
        return str(self.entry_id)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    entry = db.relationship('Post', backref='category')

    def __init__(self, name):
        self.name = name

@app.route('/')
def index():
    return "No snoop plz"


@app.route('/blog')
def blog():
    entries = Post.query.all()
    post_id = request.args.get('id')
    entry = Post.query.filter_by(entry_id=post_id).first()
    category = Post.query.join(Post.category_id).first()
    if not post_id:
        return render_template('entries.html', entries=entries, category=category)
    else:
        return render_template('entry.html', entry=entry)        

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    if request.method == 'POST':
        entry_title = request.form['title']
        entry_post = request.form['entry']
        category = request.form['category-new']
        category_exst = request.form['category-exst']
        if category == "":
            category = category_exst
        else:
            if category_exst != "":
                flash("Please don't do that")
                return render_template('new-entry.html', title=entry_title, post=entry_post, categories=retrieve_categories())
        if entry_post == "" or entry_title == "" or category == "":
            flash('Please do not leave any fields blank')
            return render_template('new-entry.html', title=entry_title, post=entry_post, categories=retrieve_categories())

        category_exists = Category.query.filter_by(name=category).first()
        if not category_exists:
            new_category = Category(category)
            db.session.add(new_category)
            db.session.commit()
            category_id = Category.query.get(new_category.id)
        else:
            category_id = Category.query.get(category_exists.id)
        new_entry = Post(entry_title, entry_post, None, category_id)
        db.session.add(new_entry)
        db.session.commit()
        new_post = Post.query.get(new_entry.entry_id)

        

        return redirect('/blog?id={0}'.format(new_post))
    return render_template('new-entry.html', categories=retrieve_categories())

def retrieve_categories():
    categories = []
    all_cats = Category.query.all()
    for cat in all_cats:
        categories.append(cat.name)
    return categories


if __name__ == '__main__':
    app.run()