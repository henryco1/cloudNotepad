from django.test import TestCase
from django.urls import resolve
from notes.views import HomePage
from django.http import HttpRequest

# Create your tests here.
class HomePageTest(TestCase):
    def testResolveRootURLToHome(self):
        found = resolve('/')
        self.assertEqual(found.func, HomePage)

    def testValidateHomePage(self):
        request = HttpRequest()
        response = HomePage(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>Notes</title>', html)
        self.assertTrue(html.endswith('</html>'))