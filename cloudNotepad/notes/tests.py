from django.test import TestCase
from django.urls import resolve
from notes.views import HomePage
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import Client

# Create your tests here.
class HomePageTest(TestCase):
    # def testResolveRootURLToHome(self):
    #     found = resolve('/')
    #     self.assertEqual(found.func, HomePage)

    def testValidateHomePage(self):
        response = self.client.get('/')
        html = response.content.decode('utf8')

        self.assertTemplateUsed(response, 'home.html')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>Notes</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))
        self.assertTemplateUsed(response, 'home.html')
        
        # request = HttpRequest()
        # response = HomePage(request)
        # html = response.content.decode('utf8')
        # expected_html = render_to_string('home.html')
        # self.assertEqual(html, expected_html)

    def testSavePOSTRequest(self):
        response = self.client.post('/', data={'item_text': 'A new note'})
        self.assertIn('A new note', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')