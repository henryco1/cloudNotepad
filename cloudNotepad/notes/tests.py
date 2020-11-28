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

    def testValidateHomePage(self):
        response = self.client.get('/')
        html = response.content.decode('utf8')

        self.assertTemplateUsed(response, 'home.html')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>Notes</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))
        self.assertTemplateUsed(response, 'home.html')

    def testSavePOSTRequest(self):
        response = self.client.post('/', data={'note_text': 'A new note'})
        self.assertIn('A new note', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')

    def testCreateReadNote(self):
        first_note = Note()
        first_note.title = 'Grocery List'
        first_note.tags = 'groceries'
        first_note.text = 'apples, bananas, citrus'
        first_note.date_created = datetime.datetime.utcnow().replace(tzinfo=utc)
        first_note.last_updated = datetime.datetime.utcnow().replace(tzinfo=utc)
        first_note.save()

        second_note = Note()
        second_note.title = 'Medicine'
        second_note.tags = 'doctor'
        second_note.text = 'take suppliments after midday meal'
        second_note.date_created = datetime.datetime.utcnow().replace(tzinfo=utc)
        second_note.last_updated = datetime.datetime.utcnow().replace(tzinfo=utc)
        second_note.save()

        saved_items = Note.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'apples, bananas, citrus')
        self.assertEqual(second_saved_item.text, 'take suppliments after midday meal')

   def testCreateNoteList(self):
        note_list = NoteList()
        NoteList.save()

        first_note = Note()
        first_note.title = 'Grocery List'
        first_note.tags = 'groceries'
        first_note.text = 'apples, bananas, citrus'
        first_note.date_created = datetime.datetime.utcnow().replace(tzinfo=utc)
        first_note.last_updated = datetime.datetime.utcnow().replace(tzinfo=utc)
        first_note.parent_list = note_list
        first_note.save()

        second_note = Note()
        second_note.title = 'Medicine'
        second_note.tags = 'doctor'
        second_note.text = 'take suppliments after midday meal'
        second_note.date_created = datetime.datetime.utcnow().replace(tzinfo=utc)
        second_note.last_updated = datetime.datetime.utcnow().replace(tzinfo=utc)
        second_note.parent_list = note_list
        second_note.save()
        
        saved_items = Note.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'apples, bananas, citrus')
        self.assertEqual(second_saved_item.text, 'take suppliments after midday meal')

        note_list.title = "Daily Notes"
        note_list.date_created = datetime.datetime.utcnow().replace(tzinfo=utc)
        note_list.last_updated = datetime.datetime.utcnow().replace(tzinfo=utc)
        note_list.notes = Notes.objects.get(parent_list=first_list.title)
        note_list.save()

        saved_items = List.objects.all()
        self.assertEqual(saved_items.count(), 1)

    def testSavePOSTRequest(self):
        self.client.post('/', data={'note_text': 'A new note'})

        self.assertEqual(Note.objects.count(), 1)
        new_item = Note.objects.first()
        self.assertEqual(new_item.text, 'A new note')


    def testRedirectAfterPOST(self):
        # Always redirect after a POST
        response = self.client.post('/', data={'note_text': 'A new note'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

        # self.assertIn('A new note', response.content.decode())
        # self.assertTemplateUsed(response, 'home.html')

    def testSaveNoPOSTRequest(self):
        # saves a POST request only if requested to/if necessary
        self.client.get('/')
        self.assertEqual(Note.objects.count(), 0)

    def testDisplayAllNotes(self):
        Note.objects.create(
            text='note1_test'
        )
        Note.objects.create(
            text='note2_test'
        )

        response = self.client.get('/')

        self.assertIn('note1_test', response.content.decode())
        self.assertIn('note2_test', response.content.decode())