from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class VisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def checkRowInTable(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def testUserViewPage(self):
        # User opens and views the homepage
        # 1. User sees the browser title
        # 2. User sees the textbox for adding template items to the list
        # 3. User sees the template list
        # 4. User sees the items in the template
        # 5. User sees their current timezone
        
        # 1
        self.browser.get('http://localhost:8000')
        self.assertIn('Notes', self.browser.title) 
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Notes', header_text)

        # 2
        input_box = self.browser.find_element_by_id('id_new_note')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a note'
        )


        self.fail('Test case incomplete')

    def testUserCreateNote(self):
        # Create functionality of the textbox
        # 1. User enters template name
        # 2. User enters template item textbox
        # 3. User presses the button that adds the item to the list
        # 4. The template list populates with the new item
        # 5. Clicking an element in the template list opens a page with the element details
        # 6. User template state is saved throughout noncontiguous sessions
        
        # 0
        self.browser.get('http://localhost:8000')

        # 2 & 3
        # why find element twice?
        input_box = self.browser.find_element_by_id('id_new_note')
        input_box.send_keys('Clean the desk')
        input_box.send_keys(Keys.ENTER)
        time.sleep(10)

        input_box = self.browser.find_element_by_id('id_new_note')
        input_box.send_keys('Wipe the keyboard')
        input_box.send_keys(Keys.ENTER)
        time.sleep(10)

        #4
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.checkRowInTable('1: Clean the desk')
        self.checkRowInTable('2: Wipe the keyboard')

        self.fail('Test case incomplete')
    
    def testUserDeleteNote(self):
        self.fail('Test case incomplete')

    def testUserUpdateNote(self):
        self.fail('Test case incomplete')

if __name__ == '__main__':
    unittest.main()