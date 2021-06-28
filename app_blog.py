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


@app.route('/')
def start():
    """
    Get list of the posts from DB and show on main page.
    Sort on id - from new to old
    A text of post is shot view (only first 100 chr)
    For full text need click on title of the post
    :return:
    Main page of blog with all posts
    """
    try:
        db = connect_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM posts ORDER BY id DESC")
        posts = cur.fetchall()
        db.close()

        param = {
            'posts': posts,
        }
    except sqlite3.Error as e:
        db.close()
        return f"Ошибка чтения базы данных... - <i>{e}</i>"

    return render_template('index.html', **param)


@app.route('/post/<int:id>')
def show_post(id):
    """
    This page show full text of choice post

    :param id:
    The id of a post from DB
    :return:
    Title and full text of the post
    """
    try:
        db = connect_db()
        res = db.cursor().execute("SELECT title, description FROM posts WHERE id=? LIMIT 1", (id, )).fetchone()
        db.close()
        if res:
            title, description = res
            return render_template('post.html', title=title, description=description)
    except sqlite3.Error as e:
        db.close()
        return f"Ошибка чтения базы данных... - <i>{e}</i>"


@app.route('/post/add')
def add_post():
    """
    Add new post. Method 'GET'
    Format request - <address>/post/add?title=<text>&description=<text>
    Function has a check for the length of the text (title and description)
    :return:
    Main page with new post
    """

    title = request.args.get("title")
    description = request.args.get("description")
    date = datetime.today().strftime("%d-%m-%Y %H:%M")

    if not title or not description:
        return redirect('/')

    data = ()

    if len(title) > 5 and len(description) > 10:
        data = (title, description, date)

    if data:
        try:
            db = connect_db()
            db.cursor().execute("INSERT INTO posts VALUES (NULL, ?, ?, ?)", data)
            db.commit()
            db.close()
        except sqlite3.Error as e:
            db.close()
            return f"Ошибка записи в базу данных... - <i>{e}</i>"

    return redirect('/')


@app.route('/post/edit')
def edit_post():
    """
    This func edit post with id from request
    New text title and description get from request
    Format request - <address>/post/edit?id=<int>&title=<text>&description=<text>
    :return:
    Main page with edited post
    """

    id = request.args.get('id')
    title = request.args.get('title')
    description = request.args.get('description')

    if not id:
        return redirect('/')

    try:
        db = connect_db()

        if title and description:
            db.cursor().execute("UPDATE posts SET title=?, description=? WHERE id=?", (title, description, id))
            db.commit()
            db.close()
            return redirect('/')
        elif title:
            db.cursor().execute("UPDATE posts SET title=? WHERE id=?", (title, id))
            db.commit()
            db.close()
            return redirect('/')
        elif description:
            db.cursor().execute("UPDATE posts SET description=? WHERE id=?", (description, id))
            db.commit()
            db.close()
            return redirect('/')
    except sqlite3.Error as e:
        db.close()
        return f"Ошибка записи в базу данных... - <i>{e}</i>"


@app.route('/post/delete')
def del_post():
    """
    This func delete post with id from request
    Format request - <address>/post/delete?id=<int>
    :return:
    Main page without deleted post
    """

    id = request.args.get('id')

    if id:
        try:
            db = connect_db()
            db.cursor().execute("DELETE FROM posts WHERE id = ?", (id, ))
            db.commit()
            db.close()
        except sqlite3.Error as e:
            db.close()
            return f"Ошибка доступа к базе данных... - <i>{e}</i>"

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)




