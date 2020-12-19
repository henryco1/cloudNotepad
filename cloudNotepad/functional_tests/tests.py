from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.select import Select
from django.test import LiveServerTestCase
from notes.models import Notebook
import unittest
import time

class VisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    """
    ================
    Helper Functions
    ================
    """

    """
    Helper function for exception handling for timeouts in functional tests
    input1: starting time of test execution
    input2: amount of time to sleep to wait for an operation in seconds
    input3: max amount of time to wait for the entire test in seconds
    input4: exception to handle
    """
    def __waitTimeExceptionHandler(self, start_time, sleep_time, max_wait_time, exception):
        if time.time() - start_time > max_wait_time:
            raise exception
        time.sleep(sleep_time)

    def __checkRowInTable(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                self.__waitTimeExceptionHandler(start_time, 0.5, 5, e)

    """
    ================
    Test Functions
    ================
    """

    """
    User opens and views the homepage
    1. User sees the browser title
    2. User sees the textbox for adding template items to the list
    3. User sees the template list
    4. User sees the items in the template
    5. User sees their current timezone
    """
    def testUserViewPage(self):
        print("=-=-=-=")
        
        print(self.live_server_url)

        print("=-=-=-=")
        # 1
        self.browser.get(self.live_server_url + "/notepad/")
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

    """
    Create functionality of the textbox
    1. 
    """
    def testUserCreateNoteList(self):
        # self.browser.get(self.live_server_url)
        pass 

    """
    Create functionality of the textbox
    1. 
    """
    def testUserCreateList(self):
        pass

    """
    Create functionality of the textbox
    1. User enters template name
    2. User enters template item textbox
    3. User presses the button that adds the item to the list
    4. The template list populates with the new item
    5. Clicking an element in the template list opens a page with the element details
    6. User template state is saved throughout noncontiguous sessions
    """
    def testUserCreateNote(self):
        # 0
        self.browser.get(self.live_server_url + "/notepad/")

        # 2 & 3
        # Each enter operation clears the input box, so we need to select the box for each subtest
        # Need to account for latency issues between the browser and the server, 
        # so we need waits and exception checks
        title_box = self.browser.find_element_by_id('id_title')
        title_box.send_keys('Cleaning Notes')
        tags_box = self.browser.find_element_by_id('id_tags')
        tags_box.send_keys('housekeeping')
        text_box = self.browser.find_element_by_id('id_text')
        text_box.send_keys('Clean the desk')

        notebook_menu = Select(self.browser.find_element_by_id('id_container'))
        notebook_menu.select_by_index(1)

        submit_button = self.browser.find_element_by_id('id_new_note')
        submit_button.send_keys(Keys.ENTER)
        time.sleep(1)

        # input_box = self.browser.find_element_by_id('id_text')
        # input_box.send_keys('Wipe the keyboard')
        # input_box.send_keys(Keys.ENTER)
        # time.sleep(1)

        #4
        # table = self.browser.find_element_by_id('id_list_table')
        # rows = table.find_elements_by_tag_name('tr')
        self.__checkRowInTable('1: Clean the desk')
        # self.__checkRowInTable('2: Wipe the keyboard')

        self.fail('Test case incomplete')
    
    def testUserDeleteNote(self):
        self.fail('Test case incomplete')

    def testUserUpdateNote(self):
        self.fail('Test case incomplete')

# if __name__ == '__main__':
#     unittest.main()