from asyncio.windows_events import NULL
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User


class Art:
    db_name = 'gallery' #check schema name

    def __init__(self, db_data):
        self.id = db_data['id']
        self.title = db_data['title']
        self.description = db_data['description']
        self.image = db_data['image']
        self.for_sale = db_data['for_sale']
        self.price = db_data['price']
        self.user_id = db_data['user_id']
        self.user = User.get_by_id({'id':db_data['user_id']})
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

# CREATE
    @classmethod
    def save(cls, data):
        query = "INSERT INTO art (user_id, collection_id, title, description, image, for_sale, price) VALUES (%(user_id)s, %(collection_id)s, %(title)s, %(description)s, %(image)s, %(for_sale)s, %(price)s );"
        return connectToMySQL(cls.db_name).query_db(query, data)

#get ALL
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM art;"
        results = connectToMySQL(cls.db_name).query_db(query)
        all_art = []
        for row in results:
            print(
                row['title'],
                row['collection'],
                row['for_sale']
                )
            all_art.append(cls(row))
        return all_art


#get ALL BY USER
    @classmethod
    def get_art_by_user(cls, data):
        query = "SELECT * FROM users LEFT JOIN art on art.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        all_user_art = []
        for row in results:
            all_user_art.append(cls(row))
        return all_user_art


#get ONE
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM art WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)

        return cls(results[0])


#EDIT/UPDATE
    @classmethod
    def update(cls, data):
        query = "UPDATE art SET collection_id = %(collection_id)s, title = %(title)s, description = %(description)s, image = %(image)s, for_sale = %(for_sale)s, price = %(price)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)


#DELETE
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM art WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)


#VALIDATION
    @classmethod
    def validate_art(art):
        is_valid = True

        if len(art['title']) < 3:
            is_valid = False
            flash("Title must be at least 3 characters")

        if len(art['description']) < 5:
            is_valid = False
            flash("Decription is required. Must be at least 5 characters.")

#check this one? 
        # if art['for_sale'] == NULL:
        #     is_valid = False
        #     flash("You must select an option ")

        return is_valid

