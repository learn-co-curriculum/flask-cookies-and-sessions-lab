#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User, ArticleSchema, UserSchema

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = [ArticleSchema().dump(a) for a in Article.query.all()]
    return make_response(articles)

@app.route('/articles/<int:id>')
def show_article(id):
    # Step 1: if this is the first request this user made, initialize page_views
    if 'page_views' not in session:
        session['page_views'] = 0

    # Step 2: increment page_views for every request to this route
    session['page_views'] = session['page_views'] + 1

    # Step 3: if user has viewed more than 3 pages, block access
    if session['page_views'] > 3:
        return {'message': 'Maximum pageview limit reached'}, 401

    # If the user is still allowed, return the article data
    article = Article.query.filter(Article.id == id).first()
    return make_response(ArticleSchema().dump(article))


if __name__ == '__main__':
    app.run(port=5555)
