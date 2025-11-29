from unittest import TestCase
from app.db.database_connection import Database


class Test(TestCase):

    def setUp(self):
        Database.setUp()

    def tearDown(self):
        Database.tearDown()
