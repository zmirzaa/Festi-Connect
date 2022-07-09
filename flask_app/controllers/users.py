from flask_app import app 
from flask import render_template, redirect, session, request, flash 
from flask_app.models.user import User 
from flask_app.models.review import Review
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index(): 
    return render_template('index.html') 


@app.route('/registerPage')
def registration(): 
    return render_template('register.html') 


@app.route('/loginPage')
def loginUser(): 
    return render_template('login.html') 

@app.route('/register', methods=['POST']) 
def register(): 
    isValid = User.validate(request.form) 
    if not isValid: 
        return redirect('/registerPage') 
    newUser = {
        'username': request.form['username'], 
        'email': request.form['email'], 
        'password': bcrypt.generate_password_hash(request.form['password'])  
    }

    id = User.save(newUser) 
    if not id: 
        flash('Something went wrong!') 
        return redirect('/registerPage') 
    session['user_id'] = id 
    return redirect('/dashboard')


@app.route('/login', methods=['POST']) 
def login(): 
    data = {
        'email': request.form['email']
    }
    user = User.getEmail(data) 
    if not user: 
        flash('That email is not in our database. Please register', "login")
        return redirect('/loginPage')
    if not bcrypt.check_password_hash(user.password, request.form['password']): 
            flash('Incorrect password', "login") 
            return redirect('/loginPage')    

    session['user_id'] = user.id 
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard(): 
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template("dashboard.html", user=User.getOne(data), reviews=Review.userReviews(data), alerts=User.getUserAlerts(data))



@app.route('/logout') 
def logout(): 
    session.clear() 
    return redirect('/')