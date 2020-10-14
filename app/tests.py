from django.test import TestCase
from django.test import Client


class ChartAnalysisEndpointTest(TestCase):

    def setUp(self):
        self.c = Client()
        return super().setUp()

    def tearDown(self):
        del self.c
        return super().tearDown()

    def test_default_params(self):
        response = self.c.get('/app/piechart/?q=trump&maxResults=10')
        self.assertEqual(200, response.status_code)

    def test_max_results(self):
        number_of_results = 2
        response = self.c.get('/app/piechart/?q=trump&maxResults=%d' % number_of_results)
        self.assertEqual(2, response.json()['results'])


class PolarityTest(TestCase):

    def setUp(self):
        self.c = Client()
        return super().setUp()

    def tearDown(self):
        del self.c
        return super().tearDown()

    def test_negative_result(self):
        pass

    def test_positive_result(self):
        pass

    def test_neutral_result(self):
        pass
