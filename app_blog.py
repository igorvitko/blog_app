from flask import Flask, render_template, request, redirect
import sqlite3
import datetime
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
    cur.execute("SELECT * FROM posts ORDER BY date DESC")
    posts = cur.fetchall()

    db.close()

    param = {
        'posts': posts,
        }

    return render_template('index.html', **param)


@app.route('/posts/add')
def add_post():

    db = connect_db()

    title = request.args.get("title")
    description = request.args.get("description")
    date = int(time.time())
    data = (title, description, date)
    # date = datetime.datetime.today().strftime("%d-%B-%Y %H:%M")

    db.cursor().execute("INSERT INTO posts VALUES (NULL, ?, ?, ?)", data)

    db.commit()
    db.close()

    return redirect('/posts')

@app.route('/posts/edit')
def edit_post():
    pass


@app.route('/posts/delete')
def del_post():
    db = connect_db()
    id = request.args.get('id')
    print(id)
    if id:
        db.cursor().execute("DELETE FROM posts WHERE id = ?", id)
        print('ok delete')

    db.commit()
    db.close()

    return redirect('/posts')


if __name__ == '__main__':
    app.run(debug=True)




