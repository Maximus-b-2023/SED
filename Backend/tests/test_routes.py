import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import pytest
from app import app, db, Users, Licences, Sales, initDB
from werkzeug.security import generate_password_hash

@pytest.fixture(scope="module")
def test_client():
    # Ensure instance directory exists
    INSTANCE_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'instance')
    os.makedirs(INSTANCE_PATH, exist_ok=True)
    
    # Use a test database
    db_path = os.path.join(INSTANCE_PATH, 'test_routes.sqlite3')
    db_uri = "sqlite:///" + db_path.replace('\\', '/') if '\\' in db_path else "sqlite:///" + db_path
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF for testing
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            # Add a test user and admin
            admin = Users(username="admin", email="admin@test.com", password=generate_password_hash("adminpw"), accounttype="Admin")
            user = Users(username="user", email="user@test.com", password=generate_password_hash("userpw"), accounttype="User")
            db.session.add(admin)
            db.session.add(user)
            db.session.commit()
            # Add a licence for sale tests
            licence = Licences(licencename="Blue Jazz", licenceprice=30, lowestsellingprice=50)
            db.session.add(licence)
            db.session.commit()
        yield client
    if os.path.exists(db_path):
        os.remove(db_path)

def login(client, username, password):
    return client.post("/login", data=dict(username=username, password=password), follow_redirects=True)

def logout(client):
    return client.get("/logout", follow_redirects=True)

def test_index_requires_login(test_client):
    response = test_client.get("/")
    assert response.status_code == 302  # Redirect to login

def test_signup_and_login_logout(test_client):
    # Signup
    response = test_client.post("/signup", data={
        "username": "newuser",
        "email": "newuser@test.com",
        "password": "newuserpw"
    }, follow_redirects=True)
    assert b"registered successfully" in response.data

    # Login
    response = login(test_client, "newuser", "newuserpw")
    assert b"index" in response.data or response.status_code == 200

    # Logout
    response = logout(test_client)
    assert b"logged out" in response.data

def test_login_invalid(test_client):
    response = login(test_client, "wronguser", "wrongpw")
    assert b"invalid" in response.data

def test_accountTypeMannager_admin_can_update(test_client):
    login(test_client, "admin", "adminpw")
    response = test_client.post("/accountTypeMannager/2", data={"accounttype": "Admin"}, follow_redirects=True)
    assert b"Account type updated successfully" in response.data

def test_users_page(test_client):
    login(test_client, "admin", "adminpw")
    response = test_client.get("/users")
    assert b"user" in response.data or response.status_code == 200

def test_licences_page(test_client):
    login(test_client, "admin", "adminpw")
    response = test_client.get("/licences")
    assert b"Blue Jazz" in response.data

def test_sales_page_admin(test_client):
    login(test_client, "admin", "adminpw")
    response = test_client.get("/sales")
    assert response.status_code == 200


def test_update_password(test_client):
    login(test_client, "user", "userpw")
    response = test_client.post("/updatePassword/2", data={
        "newpassword": "newpass123",
        "confirmpassword": "newpass123"
    }, follow_redirects=True)
    assert b"Password updated successfully" in response.data