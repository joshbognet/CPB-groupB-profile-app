from crypt import methods
import os
from flask import Flask, render_template,request, url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(basedir,'student.db')
app.config['SQLALCHEMY_TRACK_MODIFIATIONS'] = False
db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    bio = db.Column(db.Text)

    def __repr__(self):
        return f'<student {self.firstname}>'

@app.route ('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)





@app.route ('/create/',methods=('GET', 'POST'))
def create():
    if request.method  == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        age = int(request.form['age'])
        bio = request.form['bio']
        student = Student(firstname=firstname, 
        lastname=lastname, 
        email=email, 
        age=age, 
        bio=bio)
        
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('create.html')


@app.route('/<int:student_id>/edit/', methods = ['GET', 'POST'])
def update(student_id):
    student = Student.query.get_or_404(student_id)
    if request. method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        age = request.form['age']
        bio = request.form['bio']

        student.firstname = firstname
        student.lastname = lastname
        student.email = email
        student.age = age
        student.bio = bio
        db.session.add(student)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('update.html', student=student)


@app.route('/<int:student_id>/delete/')
def delete (student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ =='__main__':
    app.run(debug=True)