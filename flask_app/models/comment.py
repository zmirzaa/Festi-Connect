from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Comment:
    db = 'festiConnectSchema'
    def __init__(self, data):
        self.id  = data['id']
        self.description  = data['description']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.user_id = data['user_id']
        self.review_id = data['review_id']


    @classmethod
    def save(cls, data):
        query = 'INSERT INTO comments ( description, createdAt, updatedAt, user_id, review_id ) VALUES ( %(description)s, NOW(), NOW(), %(user_id)s, %(review_id)s );'
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM comments WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def getOneComment(cls, data):
        query = 'SELECT * from comments WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
