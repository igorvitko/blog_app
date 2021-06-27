from flask import Flask, render_template
import sqlite3
import time

app = Flask(__name__)


def connect_db():
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
                        date integer
                         )""")
    db.commit()
    db.close()


@app.route('/posts')
def start():
    db = connect_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM posts")
    posts = cur.fetchall()

    db.close()

    param = {
        'posts': posts,
        }

    return render_template('index.html', **param)


@app.route('/posts/add')
def add_post():
    pass


@app.route('/posts/edit')
def edit_post():
    pass


@app.route('/posts/delete')
def del_post():
    pass


if __name__ == '__main__':
    app.run(debug=True)




