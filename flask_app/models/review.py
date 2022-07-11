from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import comment, user
from flask import flash

class Review:
    db = 'festiConnectSchema'
    def __init__(self, data):
        self.id  = data['id']
        self.festival  = data['festival']
        self.year  = data['year']
        self.description  = data['description']
        self.tips  = data['tips']
        self.rating  = data['rating']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.user_id = data['user_id']
        self.comments = [] 
        self.likes = []
        self.users = []
        self.likesNum = 0 
        self.commentsNum = 0
        self.commenter = None



    @classmethod
    def save(cls, data):
        query = 'INSERT INTO reviews ( festival, year, rating, description, tips, createdAt, updatedAt, user_id ) VALUES ( %(festival)s, %(year)s, %(rating)s, %(description)s, %(tips)s, NOW(), NOW(), %(user_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM reviews WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def getOneReview(cls, data):
        query = 'SELECT * from reviews WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    

    @classmethod
    def likeReview(cls,data): 
        query = "INSERT INTO likes (user_id, review_id) VALUES (%(user_id)s, %(review_id)s);"
        return connectToMySQL(cls.db).query_db( query, data ) 


    #query to show all comments for one review
    @classmethod 
    def getReviewComments(cls,data):
        query = "SELECT * FROM reviews LEFT JOIN comments ON reviews.id = comments.review_id LEFT JOIN users on users.id = comments.user_id  WHERE reviews.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        review = cls(results[0])
        for row in results: 
            commentData = {
                'id': row['comments.id'],
                'description': row['comments.description'],
                'review_id': row['review_id'],
                'user_id': row['user_id'],
                'createdAt': row['comments.createdAt'],
                'updatedAt': row['comments.updatedAt']
            }
            oneComment = comment.Comment(commentData)
            oneComment.commenter = user.User.getOne({"id": row["users.id"]})
            review.comments.append(oneComment) 
        return review
    

    #query to show all reviews with num of likes
    @classmethod
    def allReviews(cls): 
        query = "Select r.id, r.festival, r.year, r.description, r.rating, r.tips, r.createdAt, r.updatedAt, r.user_id, COUNT(l.id) likes FROM reviews r LEFT JOIN likes l ON r.id = l.review_id LEFT JOIN users ON users.id = r.user_id GROUP BY r.id, r.festival, r.year, r.description, r.rating, r.tips, r.createdAt, r.updatedAt, r.user_id;"
        results = connectToMySQL(cls.db).query_db(query) 
        reviews = []
        for row in results: 
            review = cls(row) 
            review.likesNum = row['likes']
            reviews.append(review)
        return reviews
    
    #query to one review's likes info 
    @classmethod 
    def getLikerWithReview(cls,data): 
        query = "SELECT * from reviews LEFT JOIN likes on likes.review_id = reviews.id LEFT JOIN users on likes.user_id = users.id WHERE reviews.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)  
        review = cls(results[0])
        for row in results:
            likerData = {
                "id" : row["users.id"],
                "username" : row["username"], 
                "email": row['email'], 
                "password": row['password'],
                "createdAt" : row["users.createdAt"],
                "updatedAt" : row["users.updatedAt"]
            }
            review.likes.append( user.User( likerData ) )
            review.users.append(likerData["id"])
        return review


    #query to show one user's reviews
    @classmethod
    def userReviews(cls,data): 
        query = "Select r.id, r.festival, r.year, r.description, r.rating, r.tips, r.createdAt, r.updatedAt, r.user_id, COUNT(l.id) likes, COUNT(c.id) comments FROM reviews r LEFT JOIN likes l ON r.id = l.review_id LEFT JOIN comments c ON r.id = c.review_id WHERE r.user_id = %(id)s GROUP BY r.id, r.festival, r.year, r.description, r.rating, r.tips, r.createdAt, r.updatedAt, r.user_id;"
        results = connectToMySQL(cls.db).query_db(query, data) 
        reviews = []
        for row in results: 
            review = cls(row) 
            review.likesNum = row['likes']
            review.commentsNum = row['comments']
            reviews.append(review)
        return reviews


    @classmethod
    def searchReview(cls,data): 
        query = "SELECT * FROM reviews WHERE festival LIKE %(festival)s ORDER by id DESC;"
        results = connectToMySQL(cls.db).query_db(query, data)
        reviews = [] 
        for a in results:
            reviews.append(cls(a))
        return reviews 
