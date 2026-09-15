#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User, ArticleSchema, UserSchema

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t\xca\x1a\x10K'
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
    article = Article.query.filter_by(id=id).first()

    if article is None:
        return {'error': 'Article not found'}, 404

    # Get the current page views and increment
    page_views = session.get('page_views', 0)
    page_views += 1
    session['page_views'] = page_views

    # Paywall after 3 free views
    if page_views > 3:
        return {'message': 'Maximum pageview limit reached'}, 401

    return ArticleSchema().dump(article), 200

    
if __name__ == '__main__':
    app.run(port=5555)
