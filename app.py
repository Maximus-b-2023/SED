import sqlite3
from flask import Flask, jsonify, render_template, redirect, request, url_for, flash
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user, logout_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, Email
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

import os

# Load environment variables from .env file
load_dotenv()

from Backend.accountTypeMannager import authAdmin, fetchUsers, updateAccountType

#dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "./Database/tables.db"

app = Flask(__name__)
# Load secret from environment; if missing use an ephemeral key and warn.
secret = os.environ.get("FLASK_SECRET_KEY")
if not secret:
    import logging
    logging.getLogger(__name__).warning(
        "FLASK_SECRET_KEY not set — using ephemeral SECRET_KEY. "
        "Set FLASK_SECRET_KEY in Render environment variables for persistent sessions."
    )
    secret = os.urandom(24)
app.config["SECRET_KEY"] = secret
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(os.getcwd(), "instance", "db.sqlite3")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    accounttype = db.Column(db.String(50), nullable=False, default="User")

class Licences(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    licencename = db.Column(db.String(50), nullable=False)
    licenceprice = db.Column(db.String(50), nullable=False)
    lowestsellingprice = db.Column(db.Integer, nullable=False)

class Sales(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    licenceid = db.Column(db.Integer, db.ForeignKey('licences.id'), nullable=False)
    subscription = db.Column(db.String(50), nullable=False)
    quantitysold = db.Column(db.Integer, nullable=False)
    profitmade = db.Column(db.Integer, nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    licences = db.relationship('Licences', backref='sales', lazy=True)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=5, max=50)])
    email = StringField("Email", validators=[InputRequired(), Length(min=5, max=50), Email()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=80)])
    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=5, max=50)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=80)])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")

class PasswordUpdateForm(FlaskForm):
    newpassword = PasswordField("New Password", validators=[InputRequired(), Length(min=6, max=80)])
    confirmpassword = PasswordField("Confirm Password", validators=[InputRequired(), Length(min=6, max=80)])
    submit = SubmitField("Update Password")

class AccountForm(FlaskForm):
    accounttype = StringField("Account Type", validators=[InputRequired()])
    submit = SubmitField("Update Account Type")

class SaleForm(FlaskForm):
    licencename = SelectField("Licence Name", validators=[InputRequired()])
    subscription = SelectField("Subscription", validators=[InputRequired()])
    quantitysold = StringField("Quantity Sold", validators=[InputRequired()])
    revenue = StringField("Revenue", validators=[InputRequired()])
    submit = SubmitField("Add Sale")

def setAdmin():
    try:
        conn = sqlite3.connect('./instance/db.sqlite3')
    except:
        return "connection failed"
    try:
        sql = '''UPDATE users SET accounttype = 'Admin' WHERE ROWID =  1 ;'''
        conn.execute(sql)
        conn.commit()
    except:
        print("Update failed")
        return "Update failed"
    
def mockLicences():
    if not Licences.query.first():
        db.session.add(Licences(licencename="Basic", licenceprice=30, lowestsellingprice=50))
        db.session.add(Licences(licencename="Pro", licenceprice=80, lowestsellingprice=175))
        db.session.add(Licences(licencename="Bronze", licenceprice=40, lowestsellingprice=60))
        db.session.add(Licences(licencename="Silver", licenceprice=60, lowestsellingprice=40))
        db.session.add(Licences(licencename="Gold", licenceprice=70, lowestsellingprice=110))
        db.session.add(Licences(licencename="Gold ent", licenceprice=70, lowestsellingprice=110))
        db.session.add(Licences(licencename="AI", licenceprice=50, lowestsellingprice=80))
        db.session.add(Licences(licencename="Gold AI", licenceprice=100, lowestsellingprice=120))
        db.session.add(Licences(licencename="Student Bronze", licenceprice=20, lowestsellingprice=30))
        db.session.add(Licences(licencename="Concession Bronze", licenceprice=40, lowestsellingprice=30))
        db.session.commit()

def mockSales():
    if not Sales.query.first():
        db.session.add(Sales(licenceid=1, subscription="Annual", quantitysold=10, profitmade=1000, userid=1))
        db.session.add(Sales(licenceid=2, subscription="Monthly", quantitysold=5, profitmade=500, userid=1))
        db.session.add(Sales(licenceid=3, subscription="Monthly", quantitysold=15, profitmade=1500, userid=2))
        db.session.add(Sales(licenceid=4, subscription="Monthly", quantitysold=20, profitmade=2000, userid=3))
        db.session.add(Sales(licenceid=5, subscription="Annual", quantitysold=25, profitmade=2500, userid=4))
        db.session.add(Sales(licenceid=6, subscription="Monthly", quantitysold=30, profitmade=2700, userid=5))
        db.session.add(Sales(licenceid=7, subscription="Monthly", quantitysold=15, profitmade=1500, userid=6))
        db.session.add(Sales(licenceid=8, subscription="Annual", quantitysold=250, profitmade=25000, userid=7))
        db.session.add(Sales(licenceid=9, subscription="Annual", quantitysold=55, profitmade=5500, userid=8))
        db.session.add(Sales(licenceid=10, subscription="Monthly", quantitysold=75, profitmade=7500, userid=9))
        db.session.commit()
    
def initDB():
    with app.app_context():
        db.create_all()
        # Get passwords from environment variables, with fallbacks for development
        admin_pw = os.environ.get("ADMIN_PASSWORD")
        user1_pw = os.environ.get("TEST_USER1_PASSWORD")
        user2_pw = os.environ.get("TEST_USER2_PASSWORD")
        user3_pw = os.environ.get("TEST_USER3_PASSWORD")
        user4_pw = os.environ.get("TEST_USER4_PASSWORD")
        user5_pw = os.environ.get("TEST_USER5_PASSWORD")
        user6_pw = os.environ.get("TEST_USER6_PASSWORD")
        user7_pw = os.environ.get("TEST_USER7_PASSWORD")
        user8_pw = os.environ.get("TEST_USER8_PASSWORD")
        user9_pw = os.environ.get("TEST_USER9_PASSWORD")

        # Only add if not already present
        if not Users.query.filter(
        (Users.username == "Admin1") | (Users.email == "Admin1@admin.com")
        ).first():
            hashed_pw = generate_password_hash(admin_pw, method="pbkdf2:sha256")
            new_user = Users(username="Admin1", email="Admin1@admin.com", password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()
        if not Users.query.filter(
        (Users.username == "User1") | (Users.email == "User1@user.com")
        ).first():
            hashed_pw = generate_password_hash(user1_pw, method="pbkdf2:sha256")
            new_user = Users(username="User1", email="User1@user.com", password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()
        if not Users.query.filter(
        (Users.username == "User2") | (Users.email == "User2@user.com")
        ).first():
            hashed_pw = generate_password_hash(user2_pw, method="pbkdf2:sha256")
            new_user = Users(username="User2", email="User2@user.com", password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()
        if not Users.query.filter(
        (Users.username == "User3") | (Users.email == "User3@user.com")
        ).first():
            hashed_pw = generate_password_hash(user3_pw, method="pbkdf2:sha256")
            new_user = Users(username="User3", email="User3@user.com", password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()
        if not Users.query.filter(
        (Users.username == "User4") | (Users.email == "User4@user.com")
        ).first():
            hashed_pw = generate_password_hash(user4_pw, method="pbkdf2:sha256")
            new_user = Users(username="User4", email="User4@user.com", password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()
        if not Users.query.filter(
        (Users.username == "User5") | (Users.email == "User5@email.com")
        ).first():
            hashed_pw = generate_password_hash(user5_pw, method="pbkdf2:sha256")
            new_user = Users(username="User5", email="User5@email.com", password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()
        if not Users.query.filter(
        (Users.username == "User6") | (Users.email == "User6@email.com")
        ).first():
            hashed_pw = generate_password_hash(user6_pw, method="pbkdf2:sha256")
            new_user = Users(username="User6", email="User6@email.com", password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()
        if not Users.query.filter(
        (Users.username == "User7") | (Users.email == "User7@email.com")
        ).first():
            hashed_pw = generate_password_hash(user7_pw, method="pbkdf2:sha256")
            new_user = Users(username="User7", email="User7@email.com", password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()
        if not Users.query.filter(
        (Users.username == "User8") | (Users.email == "User8@email.com")
        ).first():
            hashed_pw = generate_password_hash(user8_pw, method="pbkdf2:sha256")
            new_user = Users(username="User8", email="User8@email.com", password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()
        if not Users.query.filter(
        (Users.username == "User9") | (Users.email == "User9@email.com")
        ).first():
            hashed_pw = generate_password_hash(user9_pw, method="pbkdf2:sha256")
            new_user = Users(username="User9", email="User9@email.com", password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()


        setAdmin()  # Ensure the first user is an admin
        if not Licences.query.first():
            mockLicences()
        if not Sales.query.first():
            mockSales()


@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        if Users.query.filter_by(username=form.username.data).first():
            flash("Username already exists. Please choose a different one.")
            return redirect(url_for("signup"))
        if Users.query.filter_by(email=form.email.data).first():
            flash("Email already exists. Please choose a different one.")
            return redirect(url_for("signup"))
        hashed_pw = generate_password_hash(form.password.data, method="pbkdf2:sha256")
        new_user = Users(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash("You've been registered successfully, now you can log in.")
        return redirect(url_for("login"))
    return render_template("signup.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember)
            return redirect(url_for("index"))
        flash("Your credentials are invalid.")
        return redirect(url_for("login"))
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out. See you soon!")
    return redirect(url_for("login"))

@app.route('/accountTypeMannager/<int:userid>', methods=['GET', 'POST'])
@login_required
def accountTypeMannager(userid):
    form = AccountForm()
    UID = current_user.id
    if form.validate_on_submit():
        userId = userid
        accountType = form.accounttype.data
        if updateAccountType(UID,userId, accountType) == "User " + str(userId) + " updated to account type " + accountType:
            flash("Account type updated successfully.")
        else:
            flash("Failed to update account type. You may not have permission to do this.")
        return redirect(url_for("index"))
    return render_template("accountTypeMannager.html", form=form, userid=userid)
    
@app.route('/users', methods=['GET'])
@login_required
def users():
    UID = current_user.id
    users = fetchUsers(UID)
    if isinstance(users, list):
        return render_template("users.html", users=users)
    else:
        flash("Could not fetch users.")
        return redirect(url_for("index"))

@app.route('/licences', methods=['GET'])
@login_required
def licences():
    licences = Licences.query.all()
    return render_template("licences.html", licences=licences)

@app.route('/sales', methods=['GET'])
@login_required
def sales():
    if authAdmin(current_user.id) == True:
        sales = Sales.query.all()
        return render_template("sales.html", sales=sales)
    else:
        sales = Sales.query.filter_by(userid=current_user.id).all()
        return render_template("sales.html", sales=sales)
    
@app.route('/addSale', methods=['GET','POST'])
@login_required
def addSale():
    form = SaleForm()
    form.licencename.choices = [(lic.licencename, lic.licencename )for lic in Licences.query.all()]
    form.subscription.choices = ["Monthly", "Anunual"]
    if form.validate_on_submit():
        userid = current_user.id
        licencename = form.licencename.data
        subscription = form.subscription.data
        quantitysold = form.quantitysold.data
        revenue = form.revenue.data
        
        licence = Licences.query.filter_by(licencename=licencename).first()
        if not licence:
            flash("Licence not found.")
            return redirect(url_for("addSale"))
        
        new_sale = Sales(userid=userid, licenceid=licence.id, subscription=subscription, quantitysold=quantitysold, profitmade=revenue)
        db.session.add(new_sale)
        db.session.commit()
        flash("Sale added successfully.")
        return redirect(url_for("sales"))
    
    return render_template("addSale.html", form=form)

@app.route('/deleteSale/<int:saleid>', methods=['GET','POST'])
@login_required
def deleteSale(saleid):
    sale = Sales.query.get_or_404(saleid)
    if sale.userid == current_user.id or authAdmin(current_user.id):
        db.session.delete(sale)
        db.session.commit()
        flash("Sale deleted successfully.")
    else:
        flash("You do not have permission to delete this sale.")
    return redirect(url_for("sales"))

@app.route('/updatePassword/<int:userid>', methods=['POST', 'GET'])
@login_required
def updatePassword(userid):
    form = PasswordUpdateForm()
    if form.validate_on_submit():
        if form.newpassword.data != form.confirmpassword.data:
            flash("Passwords do not match.")
            return redirect(url_for("updatePassword", userid=current_user.id))
        
        if userid == current_user.id or authAdmin(current_user.id):
            user = Users.query.get_or_404(userid)
            user.password = generate_password_hash(form.newpassword.data, method="pbkdf2:sha256")
            db.session.commit()
            flash("Password updated successfully.")
            return redirect(url_for("index"))
        else:
            flash("Permission denied. You can only update your own password.")
            return redirect(url_for("updatePassword", userid=current_user.id))

    return render_template("updatePassword.html", form=form, userid=userid)


print("App module loaded")

# if __name__ == "__main__":
#     initDB()
#     app.run()