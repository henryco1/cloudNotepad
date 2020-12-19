from django.test import TestCase
from django.urls import resolve
from notes.views import HomePage
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import Client
from notes.models import Note, Notebook
from django.utils.timezone import utc
import datetime

# Create your tests here.
class HomePageTest(TestCase):
    # def testResolveRootURLToHome(self):
    #     found = resolve('/')
    #     self.assertEqual(found.func, HomePage)

    """
    Test basic building blocks
    1. homepage
    2. post request
    3. form
    """
    def testValidateHomePage(self):
        response = self.client.get('/notepad/')
        html = response.content.decode('utf8')

        self.assertTemplateUsed(response, 'home.html')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>Notes</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))
        self.assertTemplateUsed(response, 'home.html')

    def testValidateNotebookPage(self):
        dummy_notebook = Notebook()
        dummy_notebook.save()
        
        response = self.client.get('/notepad/notebook/' + dummy_notebook.title + '/' + dummy_notebook.slug + '/')
        html = response.content.decode('utf8')

        self.assertTemplateUsed(response, 'notebook.html')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>Notebook</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))
        self.assertTemplateUsed(response, 'notebook.html')

    def testForm(self):
        response = self.client.get('/notepad/')
        html = response.content.decode('utf8')
        self.assertIn('name="title"', html)
        self.assertIn('name="tags"', html)
        self.assertIn('name="text"', html)

    """
    Test database elements
    1. note
    2. notebook
    """
    def testCreateReadNote(self):
        # Create and validate dummy notebook
        dummy_notebook = Notebook()
        dummy_notebook.title = "Elise's Notebook"
        dummy_notebook.save()

        saved_notebooks = Notebook.objects.all()
        self.assertEqual(saved_notebooks.count(), 1)   

        first_note = Note()
        first_note.title = 'Grocery List'
        first_note.tags = 'groceries'
        first_note.text = 'apples, bananas, citrus'
        first_note.container = dummy_notebook
        first_note.date_created = datetime.datetime.utcnow().replace(tzinfo=utc)
        first_note.last_updated = datetime.datetime.utcnow().replace(tzinfo=utc)
        first_note.save()

        second_note = Note()
        second_note.title = 'Medicine'
        second_note.tags = 'doctor'
        second_note.text = 'take suppliments after midday meal'
        second_note.container = dummy_notebook
        second_note.date_created = datetime.datetime.utcnow().replace(tzinfo=utc)
        second_note.last_updated = datetime.datetime.utcnow().replace(tzinfo=utc)
        second_note.save()

        saved_items = Note.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'apples, bananas, citrus')
        self.assertEqual(second_saved_item.text, 'take suppliments after midday meal')

    """
    Test for creating a notebook, which is a container of notes
    1. Test the creation of a notebook containing notes
    """
    def testCreateNotebook(self):
        first_notebook = Notebook()
        first_notebook.title = "Elise's Notebook"
        first_notebook.color = "aqua"
        first_notebook.date_created = datetime.datetime.utcnow().replace(tzinfo=utc)
        first_notebook.last_updated = datetime.datetime.utcnow().replace(tzinfo=utc)
        first_notebook.save()

        saved_notebooks = Notebook.objects.all()
        self.assertEqual(saved_notebooks.count(), 1)

        new_notebook = saved_notebooks[0]
        self.assertEqual(first_notebook.title, "Elise's Notebook")
        self.assertEqual(first_notebook.color, "aqua")

        first_note = Note()
        first_note.title = 'Grocery List'
        first_note.tags = 'groceries'
        first_note.text = 'apples, bananas, citrus'
        first_note.container = first_notebook
        first_note.date_created = datetime.datetime.utcnow().replace(tzinfo=utc)
        first_note.last_updated = datetime.datetime.utcnow().replace(tzinfo=utc)
        first_note.save()

        saved_items = Note.objects.all()
        self.assertEqual(saved_items.count(), 1)

        new_saved_item = saved_items[0]
        self.assertEqual(new_saved_item.container.title, "Elise's Notebook")

    """
    Test the display of notebooks and their contents on the notebook page
    """
    def testDisplayNotebook(self):
        my_notebook = Notebook()
        my_notebook.title = "My Notebook"
        my_notebook.color = "aqua"
        my_notebook.date_created = datetime.datetime.utcnow().replace(tzinfo=utc)
        my_notebook.last_updated = datetime.datetime.utcnow().replace(tzinfo=utc)
        my_notebook.save()

        saved_notebooks = Notebook.objects.all()
        self.assertEqual(saved_notebooks.count(), 1)

        new_notebook = saved_notebooks[0]
        self.assertEqual(my_notebook.title, "My Notebook")
        self.assertEqual(my_notebook.color, "aqua")

        # Create and validate notes for display
        Note.objects.create(
            title='note1',
            text='note1_test',
            container=my_notebook
        )
        Note.objects.create(
            title='note2',
            text='note2_test',
            container=my_notebook
        )
        # response = self.client.get('/notebook/1/')
        response = self.client.get('/notepad/notebook/' + my_notebook.title + '/' + my_notebook.slug + '/')
        # print(response.path)

        self.assertIn("My Notebook", response.content.decode())
        self.assertIn('note1_test', response.content.decode())
        self.assertIn('note2_test', response.content.decode())

    def testSavePOSTRequest(self):
        dummy_notebook = Notebook()
        dummy_notebook.save()
        response = self.client.post('/notepad/', 
          data={
            'title': 'A new note',
            'tags': '',
            'text': 'Hello World',
            'container': 'My Notebook'
        })

        self.assertEqual(Note.objects.count(), 1)
        new_item = Note.objects.first()
        self.assertEqual(new_item.title, 'A new note')
        self.assertEqual(new_item.tags, '')
        self.assertEqual(new_item.text, 'Hello World')


    def testRedirectAfterPOST(self):
        # Always redirect after a POST
        dummy_notebook = Notebook()
        dummy_notebook.save()
        response = self.client.post('/notepad/', 
          data={
            'title': 'A new note',
            'tags': '',
            'text': 'Hello World',
            'container': 'My Notebook'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/notepad/')
        # self.assertRedirects(response, '/notebook/' + dummy_notebook.slug +'/')

    def testSaveNoPOSTRequest(self):
        # saves a POST request only if requested to/if necessary
        self.client.get('/')
        self.assertEqual(Note.objects.count(), 0)

    def testDisplayAllNotes(self):
        # Create and validate dummy notebook
        dummy_notebook = Notebook()
        dummy_notebook.title = "Elise's Notebook"
        dummy_notebook.save()

        saved_notebooks = Notebook.objects.all()
        self.assertEqual(saved_notebooks.count(), 1)    

        # Create and validate notes for display
        Note.objects.create(
            title='note1',
            text='note1_test',
            container=dummy_notebook
        )
        Note.objects.create(
            title='note2',
            text='note2_test',
            container=dummy_notebook
        )

        response = self.client.get('/notepad/')

        self.assertIn('note1_test', response.content.decode())
        self.assertIn('note2_test', response.content.decode())