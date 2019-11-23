import unittest
import lib_steamprice


class GetLocalesTestCase(unittest.TestCase):

    def setUp(self):
        self.api = lib_steamprice.Api(
            url='http://api.steamprice.pro:80/v1',
            token='',
            timeout=0.5
        )

    def test_locales(self):
        locales = self.api.get_locales()

        self.assertIsInstance(locales, dict)

        self.assertIn('currencies', locales)
        self.assertIn('languages', locales)

        self.assertIn('default', locales['currencies'])
        self.assertIn('list', locales['currencies'])

        self.assertIn('default', locales['languages'])
        self.assertIn('list', locales['languages'])


class GetProductsTestCase(unittest.TestCase):

    def setUp(self):
        self.api = lib_steamprice.Api(
            url='http://api.steamprice.pro:80/v1',
            token='',
            timeout=5
        )

    def test_get_products_default(self):
        products = self.api.get_products()

        self.assertIsInstance(products, dict)

        self.assertIn('count', products)
        self.assertIn('next', products)
        self.assertIn('previous', products)
        self.assertIn('results', products)

        self.assertTrue(len(products) > 0)

        self.assertIn('id', products['results'][0])
        self.assertIn('game', products['results'][0])
        self.assertIn('name', products['results'][0])

    def test_get_products_3(self):
        products = self.api.get_products(per_page=3)

        self.assertEqual(len(products['results']), 3)

    def test_get_products_3_ru(self):
        products = self.api.get_products(per_page=3, lang=['ru'])

        self.assertEqual(len(products['results']), 3)
        self.assertIn('ru', products['results'][0]['name'])

    def test_get_products_3_ru_en(self):
        products = self.api.get_products(per_page=3, lang=['ru', 'en'])

        self.assertEqual(len(products['results']), 3)
        self.assertIn('ru', products['results'][0]['name'])
        self.assertIn('en', products['results'][0]['name'])

    def test_get_products_3_fields(self):
        products = self.api.get_products(per_page=3, fields=['price_avg'])

        self.assertEqual(len(products['results']), 3)
        self.assertIn('price_avg', products['results'][0])
        self.assertIsInstance(products['results'][0]['price_avg'], dict)

    def test_get_products_3_USD_price_avg(self):
        products = self.api.get_products(per_page=3, currency=['USD'],
                                         fields=['price_avg'])

        self.assertEqual(len(products['results']), 3)
        self.assertIn('price_avg', products['results'][0])
        self.assertIsInstance(products['results'][0]['price_avg'], dict)
        self.assertIn('USD', products['results'][0]['price_avg'])


if __name__ == '__main__':
    unittest.main()
