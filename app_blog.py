from flask import Flask

app = Flask(__name__)


@app.route('/')
def start():
    pass


@app.route('/add')
def add_post():
    pass


@app.route('/edit')
def edit_post():
    pass


@app.route('/delete')
def del_post():
    pass


if __name__ == '__main__':
    app.run(debug=True)

