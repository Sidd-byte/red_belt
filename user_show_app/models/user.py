from user_show_app.models.show import Show
from user_show_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.tv_shows = []

    @classmethod
    def save(cls,data):
        query= "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        new_user_id= connectToMySQL("red_belt").query_db(query,data)
        return new_user_id

    @staticmethod
    def validate_user(form_data):
        is_valid= True

        if len(form_data['first_name']) < 3:
            flash("Your first name must be longer than three letters","first_name")
            is_valid= False
        if len(form_data['last_name']) < 3:
            flash("Your last name must be longer than three letters","last_name")
            is_valid= False
        if not EMAIL_REGEX.match(form_data['email']):
            flash("Invalid email","email")
            is_valid= False
        if len(form_data['password']) < 8:
            flash("Your password must be longer than eight letters","password")
            is_valid= False
        if form_data['password'] != form_data['confirm_password']:
            flash("passwords do not match","confirm_password")
            is_valid= False
        return is_valid

    @classmethod
    def get_by_email(cls,data):
        query= "SELECT * FROM users WHERE email = %(email)s"
        results= connectToMySQL("red_belt").query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM tv_shows JOIN users ON users.id = tv_shows.user_id where tv_shows.id = %(id)s"
        results = connectToMySQL('red_belt').query_db(query, data)
        user = cls(results[0])

        for row in results:
            data = {
                'id' : row['id'],
                'user_id' : row['user_id'],
                'title' : row['title'],
                'network' : row['network'],
                'release_date' : row['release_date'],
                'description' : row['description'],
                'created_at' : row['created_at'],
                'updated_at' : row['updated_at']
            }

            user.tv_shows.append(Show(data))

        return user