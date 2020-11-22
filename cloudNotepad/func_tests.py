from selenium import webdriver
import unittest

class VisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def testUserViewPage(self):
        # User opens and views the homepage
        # 1. User sees the browser title
        # 2. User sees the template list
        # 3. User sees the items in the template
        # 4. User sees the textbox for adding template items to the list
        # 5. User sees their current timezone
        
        # 1
        self.browser.get('http://localhost:8000')
        self.assertIn('Notes', self.browser.title) 
        self.fail('Test case incomplete')

    def testUserCreateNote(self):
        # Create functionality of the textbox
        # 1. User enters template name
        # 2. User enters template item textbox
        # 3. User presses the button that adds the item to the list
        # 4. The template list populates with the new item
        # 5. Clicking an element in the template list opens a page with the element details
        # 6. User template state is saved throughout noncontiguous sessions
        self.fail('Test case incomplete')
    
    def testUserDeleteNote(self):
        self.fail('Test case incomplete')

    def testUserUpdateNote(self):
        self.fail('Test case incomplete')

if __name__ == '__main__':
    unittest.main()