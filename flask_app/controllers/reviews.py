from flask_app import app 
from flask import render_template, redirect, session, request, url_for
from flask_app.models.review import Review
from flask_app.models.user import User



@app.route('/addReview', methods=['POST'])
def addReview(): 
    if 'user_id' not in session : 
        return redirect('/logout')
    data = {
        "festival": request.form['festival'],
        "description": request.form['description'],
        "tips": request.form['tips'], 
        "year": request.form['year'],
        "user_id": session['user_id'],
        "rating": request.form['rating']
    }
    Review.save(data)
    print(data)
    return redirect('/dashboard')



@app.route('/delete/review/<int:id>')
def deleteReview(id):
    if 'user_id' not in session: 
        return redirect('/logout')
    data = {
        "id":id
    }
    Review.delete(data)
    return redirect('/dashboard')



@app.route('/show/review/<int:id>')
def showReview(id): 
    if 'user_id' not in session: 
        return redirect('/logout')
    data = {
        'id': id
    }
    userData = {
        "id": session['user_id']
    }
    return render_template('showReview.html', user=User.getOne(userData), users=User.getAll(), review=Review.getReviewComments(data), likes=Review.getLikerWithReview(data))



@app.route("/show/like/<int:id>")
def like(id): 
    data = {
        "review_id": id,
        "user_id": session['user_id']
    }
    Review.likeReview(data) 
    return redirect(f"/show/review/{id}")


@app.route('/show/non/review/<int:id>')
def nonShowReview(id): 
    data = {
        'id': id
    }
    return render_template('nonUserShowReview.html', users=User.getAll(), review=Review.getOneReview(data), comments=Review.getReviewComments(data), likes=Review.getLikerWithReview(data))



@app.route('/searchR', methods=['POST'])
def searchR(): 
    return redirect(url_for('searchedNonReviews', festival=request.form['festival']))



@app.route('/nonUserReviews/<festival>')
def searchedNonReviews(festival): 
    data = {
        "festival": festival
    }
    return render_template('nonUserReviews.html', users=User.getAll(), reviews=Review.searchReview(data))



@app.route('/allReviews/<festival>')
def searchedReviews(festival): 
    if 'user_id' not in session: 
        return redirect('/logout')

    userData = {
        "id": session['user_id']
    }
    data = {
        "festival": festival
    }
    return render_template('reviews.html', user=User.getOne(userData), users=User.getAll(), reviews=Review.searchReview(data))



@app.route('/searchRev', methods=['POST'])
def searchRev(): 
    return redirect(url_for('searchedReviews', festival=request.form['festival']))