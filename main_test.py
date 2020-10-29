import unittest
import os
from main import TimeCategory, TimeSubcategory, seed,\
    db, app, calc_arriendo, calc_diseno


class MyTestCase(unittest.TestCase):
    def setUp(self):
        db.session.remove()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                                os.path.join('.', 'test.db')
        self.app = app.test_client()
        f = open('oauth-private.key', 'r')
        self.key = f.read()
        f.close()

        db.create_all()
        db.session.commit()

    def test_seed(self):
        seed()
        time_categories = TimeCategory.query.all()
        self.assertEqual(7, len(time_categories))

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_arriendo(self):
        seed()
        result = calc_arriendo()
        self.assertEqual(result is not None, True)

    def test_diseno(self):
        seed()
        result = calc_diseno(2, 500)
        self.assertEqual(result is not {}, True)

if __name__ == '__main__':
    unittest.main()
