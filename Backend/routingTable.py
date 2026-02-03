from flask import Flask, request, jsonify, render_template, url_for, redirect
from signup import signup
from login import login
from flask_login import UserMixin, login_required, login_user, logout_user, current_user, LoginManager
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from accountTypeMannager import fetchUsers, updateAccountType
from flaskSession import LoginForm, RegisterForm, createUser, User
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = "login"

@app.route("/")
def home():
    return "Hello World, from Flask!"

@app.route('/signup', methods=['POST'])
def runSignup():
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "Invalid JSON input"}), 400
    username = str(data['username'])
    password = str(data['password'])
    email = str(data['email'])
    try:
        if signup(username,password,email) == "user successfully created":
            return 'signup successful'
        else:
            return 'signup failed'
    except:
        return 'signup failed'
    

# @app.route('/login', methods=['POST'])
# def runLogin():
#     try:
#         data = request.get_json()
#     except Exception as e:
#         return jsonify({"error": "Invalid JSON input"}), 400
#     email = data['email']
#     password = data['password']
#     try:
#         if login(email,password) >= 0: 
#             return 'login successful'
#         elif login(email,password) == "invalid email or password":
#                 return 'invalid email or password'
#         else:
#             return 'login failed'
#     except:
#         return 'login failed'
    
# @app.route('/AccountTypeMannager', methods=['GET', 'POST'])
# def runAccountTypeMannager():
#     try:
#         data = request.get_json()
#     except Exception as e:
#         return jsonify({"error": "Invalid JSON input"}), 400
#     targetUID = data['targetUID']
#     newAccountType = data['newAccountType']
#     UID = int(dotenv.get_key("UID"))
#     try:
#         print(fetchUsers(UID))
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#     try:
#         if updateAccountType(UID, targetUID, newAccountType) == "User " + str(UID) + " updated account type for user " + str(targetUID):
#             return 'account type updated successfully'
#         elif updateAccountType(UID, targetUID, newAccountType) == "User not verified for this action":
#             return 'user not verified for this action'
#         else:
#             return 'account type update failed'
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @app.route('/fetchUsers', methods=['POST','GET'])
# def runFetchUsers():
#     UID = int(dotenv.get_key("UID"))
#     try:
#         users = fetchUsers(UID)
#         if isinstance(users, list):
#             return jsonify(users), 200
#         else:
#             return jsonify({"error": users}), 400
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500



@app.route('/flaskRegister', methods=['GET','POST'])
def runFlaskRegister():
    form = RegisterForm()

    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data)
        createUser(form.username.data,form.email.data,hashedPassword)
        return redirect(url_for='login')

        
    return render_template('register.html', form=form)

@app.route('/flaskLogin', methods=['GET','POST'])
def runFlaskLogin():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('runDashboard'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')

@app.route('/dashboard', methods=['GET','POST'])
@login_required
def runDashboard():
    return render_template('dashboard.html')

app.run(debug=True)