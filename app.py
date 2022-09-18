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
    students=Student.query.all()#
    return render_template('index.html', students=students)

# creating a new record

@app.route('/create', methods=['GET','POST']) #In this route, you pass the  'GET', 'POST' to the methods parameter to allow both GET and POST requests. GET requests are used to retrieve data from the server. POST requests are used to post data to a specific route. By default, only GET requests are allowed. When the user first requests the /create route using a GET request, a template file called create.html will be rendered. 
def Create():
    if request.method=="POST":
       #You extract the first name, last name, email, age, and bio the user submits from the request.form object. (input form)
        fname= request.form['firstname'] 
        lname= request.form['lastname'] 
        email= request.form['email']
        age= int(request.form['age'])
        bio=request.form['bio']
        
        #You construct a student object using the Student model. 
        student= Student(
        firstname= fname,
        lastname= lname,
        email= email,
        age= age,
        bio=bio
        )
        #You add the student object to the database session, then commit the transaction.
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('Home'))
    
    return render_template('create.html')

@app.route('/<int:id>/' )
def student(id):
    student = Student.query.get_or_404(id)
    return render_template('student.html', student=student)
    

#this route /<int:id>/edit/ accepts both POST and GET methods, 
# id as a URL variable that passes the ID to the edit() view function.
@app.route('/<int:id>/edit/', methods=['GET', 'POST']) 
def edit(id):
    #the get_or_404() query method on the Student model to get the student associated with the given student ID. 
    # This will respond with a 404 Not Found error in case no student with the given ID exists in the database.
    student=Student.query.get_or_404(id)
    
    #if the given ID has a student associated with it, code execution continues to the if request.method == 'POST' condition. 
    # If the request was a GET request, meaning that the user did not submit a form, then this condition is false, and the code inside it will be skipped to the line return render_template('edit.html', student=student). 
    # This renders an edit.html template, passing it the student object you got from the database, allowing you to fill the student web form with current student data. 
    
    #When a user edits student data and submits the form, the code inside the if request.method == 'POST' is executed. 
    # You extract the submitted student data from the request.form object into corresponding variables. 
    # You set each attribute of the student object to the newly submitted data to change column values as you’ve done in Step 2. 
    # If no change was performed on a field on the web form, the value of that column will stay the same in the database.
    #After you set the student data to the newly submitted data, you add the student object to the database session, then you commit the changes. Lastly, you redirect the user to the index page.
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        age = int(request.form['age'])
        bio = request.form['bio']
    
        student.firstname = firstname
        student.lastname = lastname
        student.email = email
        student.age = age
        student.bio = bio

        db.session.add(student)
        db.session.commit()

        return redirect(url_for('Home'))

    return render_template('edit.html', student=student)



#Here, instead of using the usual app.route decorator, you use the app.post decorator 
#This means that this view function only accepts POST requests, and navigating to the /ID/delete route on your browser will return a 405 Method Not Allowed error, because web browsers default to GET requests. 
# To delete a student, the user clicks on a button that sends a POST request to this route.
@app.post('/<int:id>/delete/')
 #This delete() view function receives the ID of the student to be deleted via the student_id URL variable. 
def delete(id):
   
    # You use the get_or_404() method to get a student and save it in a student variable, or respond with a 404 Not Found in case the student doesn’t exist. You use the delete() method on the database session in the line db.session.delete(student), passing it the student object. This sets up the session to delete the student whenever the transaction is committed. Because you don’t need to perform any other modifications, you directly commit the transaction using db.session.commit(). 
    # Lastly, you redirect the user to the index page.
    student=Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('Home'))
