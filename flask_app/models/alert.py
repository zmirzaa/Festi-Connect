from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user


class Alert:
    db = 'festiConnectSchema'
    def __init__(self, data):
        self.id  = data['id']
        self.festival  = data['festival']
        self.description  = data['description']
        self.ig  = data['ig']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.user_id = data['user_id']
        self.alerter= [] 


    @classmethod
    def save(cls, data):
        query = 'INSERT INTO alerts ( festival, description, ig, createdAt, updatedAt, user_id ) VALUES ( %(festival)s,  %(description)s, %(ig)s, NOW(), NOW(), %(user_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM alerts WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def getOneAlert(cls, data):
        query = 'SELECT * from alerts WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    

    @classmethod
    def getAllAlerts(cls):
            query ="SELECT * FROM alerts;"
            results = connectToMySQL(cls.db).query_db(query)
            alerts = []

            for a in results:
                alerts.append(cls(a))
            return alerts 
    


    @classmethod
    def getAlerter(cls): 
        query = "Select * from alerts LEFT JOIN users ON users.id = alerts.user_id;"
        results = connectToMySQL(cls.db).query_db(query) 
        alerts = []
        for row in results: 
            alert = cls(row) 
            data = {
                "id" : row["users.id"],
                "username": row['username'], 
                "email": row['email'], 
                "password": row['password'],
                "createdAt" : row["users.createdAt"],
                "updatedAt" : row["users.updatedAt"]
            }
            alert.alerter = user.User(data)
            alerts.append(alert)
        return alerts