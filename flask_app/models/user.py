from flask_app.config.mysqlconnection import connectToMySQL 
from flask import flash 
from flask_app.models import alert, review
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User: 
    db = 'festiConnectSchema'
    def __init__(self,data): 
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.reviews = [] 
        self.alerts = []


    @staticmethod
    def validate(user):
        isValid = True
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(User.db).query_db(query,user)
        print(results)
        if len(results) >= 1:
            isValid = False
            flash("That email is already taken!", "register")
        if not EMAIL_REGEX.match(user['email']):
            isValid = False
            flash("Invalid email format.", "register")
        if len(user['username']) < 3:
            isValid = False
            flash('Username must be at least 3 characters long.', "register")
        if len(user['password']) < 8:
            isValid = False
            flash('Password must be at least 8 characters long', "register")
        if user['password'] != user['confirm']:
            isValid = False
            flash('Passwords do not match', "register")
        return isValid
    

    @classmethod 
    def getOne(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s;' 
        results = connectToMySQL(cls.db).query_db(query, data) 
        if len(results) < 1: 
            return False 
        return cls(results[0]) 
        
    @classmethod
    def getAll(cls): 
        query = 'SELECT * FROM users;' 
        results = connectToMySQL(cls.db).query_db(query) 
        users = [] 
        for u in results: 
            users.append(cls(u))
        return users 

    @classmethod 
    def getEmail(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;' 
        results = connectToMySQL(cls.db).query_db(query, data) 
        if len(results) < 1: 
            return False 
        return cls(results[0]) 
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( username , email , password, createdAt, updatedAt ) VALUES ( %(username)s , %(email)s , %(password)s, NOW() , NOW() );"
        return connectToMySQL(cls.db).query_db( query, data )
    


    #query to show all of user's alerts
    @classmethod 
    def getUserAlerts(cls,data):
        query = "SELECT * FROM users LEFT JOIN alerts ON users.id = alerts.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        alerts = []
        for row in results: 
            alertData = {
                'id': row['alerts.id'],
                'festival': row['festival'],
                'ig': row['ig'],
                'description': row['description'],
                'user_id': row['user_id'],
                'createdAt': row['alerts.createdAt'],
                'updatedAt': row['alerts.updatedAt']
            }
            alerts.append(alert.Alert(alertData)) 
        return alerts 
    
    
