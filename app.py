from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
from functools import wraps
import os
import secrets

load_dotenv()

AUTH_KEY = os.getenv("AUTH_KEY")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.getenv("SECRET_KEY") or secrets.token_hex(32)

db = SQLAlchemy(app)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    content = db.Column(db.String(25000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Post %r' % self.id


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        entered = request.form.get('password', '')
        if AUTH_KEY and secrets.compare_digest(entered, AUTH_KEY):
            session['logged_in'] = True
            next_url = request.args.get('next') or url_for('admin')
            return redirect(next_url)
        error = 'Incorrect password'
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/blog')
def blog():
    posts = Posts.query.order_by(Posts.date_created.desc()).all()
    return render_template('blog.html', posts=posts)


@app.route('/admin', methods=['POST', 'GET'])
@login_required
def admin():
    if request.method == 'POST':
        blog_content = request.form.get('post-body')
        blog_title = request.form.get('post-title')
        new_blog_post = Posts(title=blog_title, content=blog_content)
        db.session.add(new_blog_post)
        db.session.commit()
        return redirect('/admin')
    else:
        posts = Posts.query.order_by(Posts.date_created.desc()).all()
        return render_template('admin.html', posts=posts)


@app.route('/delete-post/<int:id>', methods=['POST', 'GET'])
@login_required
def delete(id):
    post_to_delete = Posts.query.get_or_404(id)
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        return redirect('/admin')
    except:
        return 'i guess we will have to live with that one'


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)