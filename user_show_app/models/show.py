from user_show_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Show:
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.created_at = data['created_at']

    @staticmethod
    def validate_show(form_data):
        is_valid= True
        if len(form_data['title']) < 3:
            flash("Your title must be longer than three letters","title")
            is_valid= False
        if form_data['release_date'] == "":
            flash("date must be given","release_date")
            is_valid= False
        if len(form_data['network']) < 3:
            flash("Your network must be longer than three letters","network")
            is_valid= False
        if len(form_data['description']) < 3:
            flash("Your description must be longer than three letters","description")
            is_valid= False
        return is_valid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO tv_shows (user_id, title, release_date, network, description) VALUES (%(user_id)s,%(title)s,%(release_date)s,%(network)s,%(description)s);"
        new_show_id = connectToMySQL('red_belt').query_db(query,data)
        return new_show_id