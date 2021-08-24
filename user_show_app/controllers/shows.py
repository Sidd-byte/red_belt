from user_show_app import app
from flask import render_template, redirect, request, session, flash
from user_show_app.models.show import Show

@app.route('/new')
def new_show():
    return render_template('add_show.html')

@app.route('/new', methods = ['post'])
def create_show():

    if not Show.validate_show(request.form):
        return redirect('/new')

    data = {
        'title' : request.form['title'],
        'network' : request.form['network'],
        'description' : request.form['description'],
        'release_date' : request.form['release_date'],
        'title' : request.form['title'],
        'user_id' : session['logged_user']
    }
    new_show_id = Show.save(data)
    return redirect('/dashboard')

@app.route('/show/edit')
def edit_show():
    return render_template('edit_show.html')