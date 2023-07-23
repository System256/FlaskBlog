from flask import Flask, render_template, url_for, request, redirect
from app.db import db
from app.config import Config
from app.models import Article


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    @app.route('/')
    @app.route('/home')
    def index():
        return render_template('index.html')


    @app.route('/about')
    def about():
        return render_template('about.html')


    @app.route('/posts')
    def posts():
        articles = Article.query.order_by(Article.date.desc()).all()
        print(articles)
        return render_template('posts.html', articles=articles)


    @app.route('/posts/<int:id>')
    def post_detail(id):
        article = Article.query.get(id)
        return render_template('post_detail.html', article=article)


    @app.route('/posts/delete/<int:id>')
    def post_delete(id):
        article = Article.query.get_or_404(id)

        try:
            db.session.delete(article)
            db.session.commit()
            return redirect(url_for('posts'))
        except Exception as exc:
            return f'При удалении статьи произошла ошибка {exc}'


    @app.route('/posts/edit/<int:id>', methods=['POST', 'GET'])
    def post_update(id):
        article = Article.query.get(id)
        if request.method == 'POST':
            article.title = request.form['title']
            article.intro = request.form['intro']
            article.text = request.form['text']

            try:
                db.session.commit()
                return redirect(url_for('posts'))
            except Exception as exc:
                return f'При редактировании статьи произошла ошибка {exc}'
        else:
            return render_template('post_edit.html', article=article)


    @app.route('/posts/add', methods=['POST', 'GET'])
    def add_post():
        if request.method == 'POST':
            title = request.form['title']
            intro = request.form['intro']
            text = request.form['text']

            article = Article(title=title, intro=intro, text=text)

            try:
                db.session.add(article)
                db.session.commit()
                return redirect(url_for('posts'))
            except Exception as exc:
                return f'При добавлении статьи произошла ошибка {exc}'
        else:
            return render_template('add_article.html')
        
    
    return app