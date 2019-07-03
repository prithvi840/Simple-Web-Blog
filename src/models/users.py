from src.common.database import Database
import src.models.errors as UserError
from src.common.utils import Utils
from src.models.blog import Blog
import uuid
import datetime
from flask import session

class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_email(cls, email):
        data =Database.find_one(collection="users", query={"email": email})
        if data is not None:
            return cls(**data)


    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one(collection="users", query={"_id": _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email, password):
        user = User.get_by_email(email)
        if user is not None:
            return user.password == password

        return False

    @classmethod
    def register(cls, email, password):
        user = cls.get_by_email(email)
        if user is not None:
            raise UserError.UserAlreadyRegisteredError("Email already exsists")
        if not Utils.email_is_valid(email):
            raise UserError.InvalidEmailError("The Email is not in correct format")

        new_user = cls(email, password)
        new_user.save_to_mongo()
        return True


    @staticmethod
    def login(user_email):
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    def get_blogs(self):
        return Blog.find_by_author_id(self._id)

    def new_blog(self, title, description):
        blog = Blog(author= self.email,
                    title= title,
                    description= description,
                    author_id = self._id)

        blog.save_to_mongo()

    @classmethod
    def list_users(cls):
        user = Database.find(collection="users", query="{}")
        if user is not None:
            return cls(**user)

    @staticmethod
    def new_post(blog_id, title, content, date= datetime.datetime.utcnow()):
        blog = Blog.from_mongo(blog_id)
        blog.new_post(title= title,
                      content = content,
                      date = date)


    def json(self):
        return {
            "email": self.email,
            "_id": self._id,
            "password": self.password
        }

    def save_to_mongo(self):
        Database.insert(collection="users", data =self.json())


