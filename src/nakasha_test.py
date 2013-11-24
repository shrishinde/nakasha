import os
import nakasha
import unittest
import tempfile

class NakashaTestCase(unittest.TestCase):

    def setUp(self):
        """Before each test, set up a blank database"""
        self.db_fd, nakasha.app.config['DATABASE'] = tempfile.mkstemp()
        nakasha.app.config['TESTING'] = True
        self.app = nakasha.app.test_client()
        nakasha.init_db()
        rooms  = [
            ('Apple','Pune','Baner','A','W1','4'),
            ('Orange','Pune','Baner','A','W1','4'),
            ('Mango','Pune','Baner','A','W1','4'),
            ('Raspberry','Pune','Baner','A','W1','1')
        ]
        query = 'INSERT INTO room (name, city, site, building, wing, floor) VALUES (?,?,?,?,?,?)'
        nakasha.insert_data(query, rooms)
        
        

    def tearDown(self):
        """Get rid of the database again after each test."""
        os.close(self.db_fd)
        os.unlink(nakasha.app.config['DATABASE'])

        
    # testing functions
    def test_rooms(self):
        """ Test that rooms resource work well """
        rv = self.app.get("/api/rooms")
        assert b'Apple' in rv.data
    
    def test_room(self):
        """ Test that single room works well"""
        rv = self.app.get("/api/rooms/Mango")
        assert b'Mango' in rv.data

if __name__ == '__main__':
    unittest.main()
