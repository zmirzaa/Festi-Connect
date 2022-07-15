from flask_app import app 
from flask import render_template, redirect, session, request 
from flask_app.models.comment import Comment




@app.route('/createComment', methods=['POST'])
def createCom(): 
    if 'user_id' not in session : 
        return redirect('/logout')
    data = {
        "description": request.form['description'],
        "user_id": session['user_id'],
        "review_id": request.form['review_id']
    }
    Comment.save(data)
    return redirect(f"/show/review/{request.form['review_id']}")

