from flask_app import app 
from flask import render_template, redirect, session, request, url_for 
from flask_app.models.alert import Alert
from flask_app.models.user import User
from flask_app.models.review import Review


@app.route('/addAlert', methods=['POST'])
def addAlert(): 
    if 'user_id' not in session : 
        return redirect('/logout')
    data = {
        "festival": request.form['festival'],
        "ig": request.form['ig'],
        "description": request.form['description'], 
        "user_id": session['user_id']
    }
    Alert.save(data)
    return redirect("/dashboard")



@app.route('/delete/alert/<int:id>')
def deleteAlert(id):
    if 'user_id' not in session: 
        return redirect('/logout')
    data = {
        "id":id
    }
    Alert.delete(data)
    return redirect('/dashboard')



@app.route('/allAlerts')
def showAlerts(): 
    if 'user_id' not in session: 
        return redirect('/logout')
    userData = {
        "id": session['user_id']
    }
    return render_template('alerts.html', user=User.getOne(userData), users=User.getAll(), alerts=Alert.getAlerter())



@app.route('/nonUserAlerts')
def showNonUserAlerts(): 
    return render_template('nonUserAlerts.html', alerts=Alert.getAlerter())


@app.route('/searchA', methods=['POST'])
def searchA(): 
    return redirect(url_for('searchedNonAlerts', festival=request.form
    ['festival']))


@app.route('/searchedNonAlerts/<festival>')
def searchedNonAlerts(festival): 
    data = {
        "festival": festival
    }
    return render_template('nonUserAlerts.html', users=User.getAll(), alerts=Alert.searchAlert(data))



@app.route('/searchAlert', methods=['POST'])
def searchAlert(): 
    return redirect(url_for('searchedAlerts', festival=request.form['festival']))



@app.route('/searchedAlerts/<festival>')
def searchedAlerts(festival): 
    if 'user_id' not in session: 
        return redirect('/logout')

    userData = {
        "id": session['user_id']
    }
    data = {
        "festival": festival
    }
    return render_template('alerts.html', user=User.getOne(userData), users=User.getAll(), alerts=Alert.searchAlert(data))