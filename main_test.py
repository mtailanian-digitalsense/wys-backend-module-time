import unittest
import os
from main import TimeCategory, TimeSubcategory, seed,\
    db, app, calc_arriendo, calc_diseno, calc_licitacion,\
    SubCategoryConstants, calc_construccion, calc_mudanza, calc_marcha_blanca


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

    def test_licitacion(self):
        seed()
        result = calc_licitacion(True)
        self.assertEqual(result is not {}, True)
        subcat : dict
        for subcat in result['subcategories']:
            self.assertEqual(subcat['weeks'], 0)

        result = calc_licitacion(False)

        dict_values = {
            SubCategoryConstants.LICITACION_OBRA: 4,
            SubCategoryConstants.NEGOCIACION: 2,
            SubCategoryConstants.ADJUDICACION_Y_FIRMA: 0
        }

        for subcat in result['subcategories']:
            weeks = dict_values[subcat['code']]
            self.assertEqual(weeks, subcat['weeks'])

    def test_construccion(self):
        seed()
        result = calc_construccion(5000, 'free', demolition_required=True, construction_mod='turnkey')
        self.assertEqual(result is not {}, True)

    def test_mudanza(self):
        seed()
        result = calc_mudanza()
        self.assertEqual(result is not {}, True)

    def test_marcha_blanca(self):
        seed()
        result = calc_marcha_blanca(5000)
        self.assertEqual(result is not {}, True)

if __name__ == '__main__':
    unittest.main()
