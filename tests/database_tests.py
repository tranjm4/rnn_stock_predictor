import unittest
from api_scraper.database import *

class DatabaseTests(unittest.TestCase):
    def test_create_database_makes_table(self):
        try:
            clear_database()
            connection, cursor = connect_to_db()
            
            cursor.execute("SELECT * FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            tables = [x[0] for x in tables]
            self.assertIn("Day", tables)
            self.assertIn("Stock", tables)
        except:
            print("Error: DB Connection")
            self.assertEquals(0, 1)
        finally:
            connection.close()
            
if __name__ == "__main__":
    unittest.main()