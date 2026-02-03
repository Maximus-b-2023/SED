from flask_login import UserMixin, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_sqlalchemy import SQLAlchemy
from routingTable import app
import sqlite3

db = SQLAlchemy(app)

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placehodler":"Username"})
    
    email = StringField(validators=[InputRequired(), Length(
        min=4, max=30)], render_kw={"placehodler":"Email"})
    
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placehodler":"Password"})
    
    submit = SubmitField("Register")

    def validateEmail(self, email):
        conn = sqlite3.connect('./instance/db.sqlite3')
        cur = conn.cursor()
        sql = '''SELECT FROM users WHERE email = (?)'''
        params = email
        try:
            existingEmail = cur.execute(sql,params)
            raise ValidationError(
                "That email is already registered"
            )
        except:
            return True

class LoginForm(FlaskForm):    
    email = StringField(validators=[InputRequired(), Length(
        min=4, max=30)], render_kw={"placehodler":"Email"})
    
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placehodler":"Password"})
    
    submit = SubmitField("Login")

def createUser(username,email,password):
    conn = sqlite3.connect('./instance/db.sqlite3')
    sql = '''INSERT INTO users (USERNAME,PASSWORD,EMAIL,ACCOUNTTYPE) VALUES(?,?,?,?)''' 
    params = (username, password, email, "User")
    try:
        conn.execute(sql, params)
        conn.commit()
        return "Insert success"
    except:
        return "Insert failed"
    

class User(UserMixin):
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password
        self.authenticated = False

    def is_active(self):
        return self.is_active()

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True

    def get_id(self):
        return self.id