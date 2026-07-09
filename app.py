from flask import Flask, url_for, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(25000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return 'Post %r' %self.id

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blog')
def blog():
    posts = Posts.query.order_by(Posts.date_created.desc()).all()
    return render_template('blog.html', posts=posts)

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        blog_content = request.form.get('post-body')
        new_blog_post = Posts(content=blog_content)
        db.session.add(new_blog_post)
        db.session.commit()
        return redirect('/admin')
    else:
        posts = Posts.query.order_by(Posts.date_created.desc()).all()
        return render_template('admin.html', posts=posts)

@app.route('/delete-post/<int:id>', methods=['POST', 'GET'])
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
    
    app.run()