import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


app = Flask(__name__)
app.config['SECRET_KEY'] = 'q1w2e3r4t5y6'


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)
   

# @app.route('/create', methods=('GET', 'POST'))
# def create():
      
#             return render_template('create.html')

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        user = request.form['user']
        phnno = request.form['phnno']

        if not user:
            flash('user is required!')
           
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (user, phnno) VALUES (?, ?)',
                         (user, phnno))
            conn.commit()
            conn.close()
            flash('added Successfully')
            return redirect(url_for('index'))
            

    return render_template('create.html')


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        user = request.form['user']
        phnno = request.form['phnno']

        if not user:
            flash('user is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET user = ?, phnno = ?'
                         ' WHERE id = ?',
                         (user, phnno, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)



if __name__ == '__main__':
    app.run(debug=True)


    

    