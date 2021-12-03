from app import db
from datetime import datetime as dt, timedelta
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
import secrets


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))



    def save(self):
        db.session.add(self)
        db.session.commit() 

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    img = db.Column(db.String)
    created_on = db.Column(db.DateTime, index=True, default=dt.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
   

    def __repr__(self):
        return f'<Item: {self.id} | {self.name}>'

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        data={
            'id':self.id,
            "name":self.name,
            "price":self.price,
            "img":self.img,
            "created_on":self.created_on,
            "user_id":self.user_id
        }
        return data

    def from_dict(self, data):
        for field in ["name","price","img","user_id"]:
            if field in data:
                setattr(self,field, data[field])
    
    
    

   


# class Category(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200))
#     products = db.relationship('Item', cascade ='all, delete-orphan',  backref="category")

#     def __repr__(self):
#         return f'<Catergoy: {self.id} | {self.name}>'

#     def save(self):
#         db.session.add(self)
#         db.session.commit()
    
#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()

#     def to_dict(self):
#         data={
#             "id": self.id,
#             "name": self.name
#         }
#         return data


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    created_on =db.Column(db.DateTime, default=dt.utcnow)
    

    def buy_items(self, item):
        cart_entry= Cart(user_id =current_user.id, item_id = item.id)
        cart_entry.save()
    
    def remove_items(self, item):
        cart_remove= self.remove(item)
        cart_remove.save()



    def __repr__(self):
        return f'<User: {self.id} | {self.email}>'
    
    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])
    
    def hash_password(self, original_password):
        return generate_password_hash(original_password)
    
    def check_password_hash(self, login_password):
        return check_password_hash(self.password, login_password)

    def save(self):
        db.session.add(self)
        db.session.commit() 

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


