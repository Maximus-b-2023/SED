import sys
import os
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app import app, db, Users, Crops, Sales, setAdmin, mockCrops, mockSales, initDB

TEST_DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'instance', 'test_db.sqlite3')
TEST_DB_URI = "sqlite:///" + os.path.abspath(TEST_DB_PATH)

class BusinessLogicTestCase(unittest.TestCase):
    def setUp(self):
        # Use a fresh test database for each test
        app.config["SQLALCHEMY_DATABASE_URI"] = TEST_DB_URI
        app.config["TESTING"] = True
        self.app = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        # Remove the test database file
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def test_initDB_creates_users_and_admin(self):
        with app.app_context():
            initDB()
            users = Users.query.all()
            self.assertGreaterEqual(len(users), 1)
            admin = Users.query.filter_by(username="Admin1").first()
            self.assertIsNotNone(admin)
            self.assertEqual(admin.accounttype, "Admin")

    def test_mockCrops_adds_crops(self):
        with app.app_context():
            mockCrops()
            crops = Crops.query.all()
            self.assertGreaterEqual(len(crops), 1)
            self.assertTrue(any(c.cropname == "Blue Jazz" for c in crops))

    def test_mockSales_adds_sales(self):
        with app.app_context():
            # Add required users and crops first
            db.session.add(Users(username="User1", email="u1@u.com", password="pw", accounttype="User"))
            db.session.add(Crops(cropname="Blue Jazz", seedprice=30, lowestsellingprice=50))
            db.session.commit()
            mockSales()
            sales = Sales.query.all()
            self.assertGreaterEqual(len(sales), 1)

    def test_setAdmin_sets_first_user_admin(self):
        with app.app_context():
            user = Users(username="TestUser", email="test@user.com", password="pw", accounttype="User")
            db.session.add(user)
            db.session.commit()
            setAdmin()
            updated_user = Users.query.get(1)
            self.assertEqual(updated_user.accounttype, "Admin")

if __name__ == "__main__":
    unittest.main()