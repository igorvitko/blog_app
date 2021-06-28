from datetime import datetime
from flask import Flask, render_template, request, redirect
import sqlite3



app = Flask(__name__)


def connect_db():
    """

    :return:
    new connection with DB
    """
    connection = sqlite3.connect('blog.sqlite')
    connection.row_factory = sqlite3.Row
    return connection


def create_db():
    """
    This function create DB.
    Need execute this function once from console
    :return:
    New DB if not exit one
    """
    db = connect_db()
    db.cursor().execute(""" CREATE TABLE IF NOT EXISTS posts
                        (id integer PRIMARY KEY AUTOINCREMENT,
                        title text NOT NULL,
                        description text NOT NULL,
                        date text
                         )""")
    db.commit()
    db.close()


@app.route('/posts')
def start():
    """
    Get all posts from DB and view on page.
    Sort on id - from new to old
    :return:
    Main page of blog with all posts
    """
    db = connect_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = cur.fetchall()

    db.close()

    param = {
        'posts': posts,
        }

    return render_template('index.html', **param)


@app.route('/posts/add')
def add_post():
    """
    Add new post. Method 'GET'
    Format request - <address>/posts/add?title=<text>&description=<text>
    Function has a check for the length of the text (title and description)
    :return:
    Main page with new post
    """
    db = connect_db()

    title = request.args.get("title")
    description = request.args.get("description")
    date = datetime.today().strftime("%d-%m-%Y %H:%M")

    data = ()

    if len(title) > 5 and len(description) > 10:
        data = (title, description, date)

    if data:
        db.cursor().execute("INSERT INTO posts VALUES (NULL, ?, ?, ?)", data)

    db.commit()
    db.close()

    return redirect('/posts')


@app.route('/posts/edit')
def edit_post():
    """
    This func edit post with id from request
    New text title and description get from request
    Format request - <address>/posts/edit?id=<int>&title=<text>&description=<text>
    :return:
    Main page with edited post
    """
    db = connect_db()

    id = request.args.get('id')
    title = request.args.get('title')
    description = request.args.get('description')

    db.cursor().execute("UPDATE posts SET title=?, description=? WHERE id=?", (title, description, id))

    db.commit()
    db.close()

    return redirect('/posts')

@app.route('/posts/delete')
def del_post():
    """
    This func delete post with id from request
    Format request - <address>/posts/delete?id=<int>
    :return:
    Main page without deleted post
    """
    db = connect_db()
    id = request.args.get('id')

    if id:
        db.cursor().execute("DELETE FROM posts WHERE id = ?", id)

    db.commit()
    db.close()

    return redirect('/posts')


if __name__ == '__main__':
    app.run(debug=True)




