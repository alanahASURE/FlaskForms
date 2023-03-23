import sqlite3

from flask import Flask, render_template, redirect, url_for, flash, redirect, request, abort
from forms import SurveyForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

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

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')

        elif not content:
            flash('Content is required!')

        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

survey_list = [{
    'name': 'Lana',
    'age': 24,
    'email': 'alanah10bell10@gmail.com',
    'zipcode': 85281
}]


@app.route('/', methods=('GET', 'POST'))
def index():
    form = SurveyForm()
    if form.validate_on_submit():
        survey_list.append({
            'name': form.name.data,
            'age': form.age.data,
            'email': form.email.data,
            'zipcode': form.zipcode.data
        })
        return redirect(url_for('survey'))
    #database
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()

    return render_template('index.html', form=form, posts=posts)


@app.route('/survey/')
def survey():
    return render_template('survey.html', survey_list=survey_list)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')