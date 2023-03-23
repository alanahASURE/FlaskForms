import sqlite3

from flask import Flask, render_template, redirect, url_for, flash, redirect, request, abort
from forms import SurveyForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_survey(survey_id):
    conn = get_db_connection()
    survey = conn.execute('SELECT * FROM surveys WHERE id = ?',
                        (survey_id,)).fetchone()
    conn.close()
    if survey is None:
        abort(404)
    return survey

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    survey = get_survey(id)

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        zipcode = request.form['zipcode']

        if not name:
            flash('Name is required!')
        elif not age:
            flash('Age is required!')
        elif not email:
            flash('Email is required!')
        elif not zipcode:
            flash('Zip code is required!')

        else:
            conn = get_db_connection()
            conn.execute('UPDATE surveys SET name = ?, age = ?, email = ?, zipcode = ?'
                         ' WHERE id = ?',
                         (name, age, email, zipcode, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', survey=survey)

@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    survey = get_survey(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM surveys WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(survey['name']))
    return redirect(url_for('index'))

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
    surveys = conn.execute('SELECT * FROM surveys').fetchall()
    conn.close()
    return render_template('index.html', surveys=surveys)


@app.route('/survey/')
def survey():
    return render_template('survey.html', survey_list=survey_list)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        zipcode = request.form['zipcode']

        if not name:
            flash('Name is required!')
        elif not age:
            flash('Age is required!')
        elif not email:
            flash('Email is required!')
        elif not zipcode:
            flash('Zip code is required!')
        else:
            conn = get_db_connection()
            conn.execute("INSERT INTO surveys (name, age, email, zipcode) VALUES (?, ?, ?, ?)",
                        (name, age, email, zipcode))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')