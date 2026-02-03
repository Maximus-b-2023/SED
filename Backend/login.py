import sqlite3
import os

def setup_test_db():
    # Ensure the instance directory exists
    os.makedirs('./instance', exist_ok=True)
    # Create a fresh test database
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    conn = sqlite3.connect(TEST_DB)

def login(email,password):
    try:
        conn = sqlite3.connect('./instance/db.sqlite3')
        cur = conn.cursor()
    except:
        return "connection failed"
    try:
        sql = '''SELECT ROWID, USERNAME from users WHERE EMAIL = (?) AND PASSWORD = (?)'''
        params = (email, password)
        cur.execute(sql,params)
        creds = cur.fetchall()
        return int(creds)
    except:
        print("invalid email or password")
        return "invalid email or password"

def getUsername(UID):
    try:
        conn = sqlite3.connect('./instance/db.sqlite3')
        cur = conn.cursor()
    except:
        return "connection failed"
    try:
        sql = '''SELECT USERNAME FROM users WHERE ROWID = (?)'''
        params = (UID,)
        cur.execute(sql,params)
        username = cur.fetchone()
        return username[0]
    except:
        print("Username retrieval failed")
        return "Username retrieval failed"
