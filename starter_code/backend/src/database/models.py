#-----------------------------------------------------------#
# Imports.
#-----------------------------------------------------------#
import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

#-----------------------------------------------------------#
# Database path.
#-----------------------------------------------------------#
database_path = "sqlite:///database.db"

#-----------------------------------------------------------#
# Connection database.
#-----------------------------------------------------------#
db = SQLAlchemy()


#-----------------------------------------------------------#
# Setup.
#-----------------------------------------------------------#
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


#-----------------------------------------------------------#
# Drop database and create.
#-----------------------------------------------------------#
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    drink = Drink(
        title='water',
        recipe='[{"name": "water", "color": "blue", "parts": 1}]'
    )
    drink.insert()


#-----------------------------------------------------------#
# Class Drink.
#-----------------------------------------------------------#
class Drink(db.Model):
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    title = Column(String(80), unique=True)
    recipe = Column(String(180), nullable=False)

    #-----------------------------------------------------------#
    # short().
    #-----------------------------------------------------------#
    def short(self):
        print(json.loads(self.recipe))
        load = json.loads(self.recipe)
        sh_recipe = [{'color': r['color'], 'parts': r['parts']} for r in load]
        return {
            'id': self.id,
            'title': self.title,
            'recipe': sh_recipe
        }

    #-----------------------------------------------------------#
    # long().
    #-----------------------------------------------------------#
    def long(self):
        return {
            'id': self.id,
            'title': self.title,
            'recipe': json.loads(self.recipe)
        }

    #-----------------------------------------------------------#
    # insert().
    #-----------------------------------------------------------#
    def insert(self):
        db.session.add(self)
        db.session.commit()

    #-----------------------------------------------------------#
    # delete().
    #-----------------------------------------------------------#
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    #-----------------------------------------------------------#
    # update().
    #-----------------------------------------------------------#
    def update(self):
        db.session.commit()

    #-----------------------------------------------------------#
    # __repr__.
    #-----------------------------------------------------------#
    def __repr__(self):
        return json.dumps(self.short())
