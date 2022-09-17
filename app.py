import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer)
    bio =db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default = func.now() )
    
    
    def __repr__(self):
        return f'<student {self.firstname}>'




@app.route('/')
def Home():
    students=Student.query.all()
    return render_template('index.html', students = students)

@app.route('/Create', methods=['GET', 'POST'])
def Create():
    if request.method=="POST":
        fname = request.form['firstname']
        lname = request.form['lastname']
        email = request.form['email']
        age = int(request.form['age'])
        bio =request.form['bio']

        student= Student(
        firstname = fname,
        lastname = lname,
        email = email,
        age = age,
        bio = bio
        )
        
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('Home'))

    return render_template('create.html')

@app.route('/<int:student_id>/')
def student(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('student.html', student = student)


@app.route('/<int:student_id>/update', methods = ('GET', 'POST'))
def Update(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method=="POST":
        fname = request.form['firstname']
        lname = request.form['lastname']
        email = request.form['email']
        age = int(request.form['age'])
        bio =request.form['bio']
        
        firstname = fname,
        lastname = lname,
        email = email,
        age = age,
        bio = bio

        db.session.add(student)
        db.session.commit()
        return redirect(url_for('Home'))

    return render_template('update.html', student = student)

@app.post('/<int:student_id>/delete')
def Delete(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('Home'))