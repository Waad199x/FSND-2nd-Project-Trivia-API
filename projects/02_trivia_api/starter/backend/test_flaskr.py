import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db,Question, Category


class TriviaAppTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        self.DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')  
        self.DB_USER = os.getenv('DB_USER', 'postgres')  
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')  
        self.DB_NAME = os.getenv('DB_NAME', 'trivia_test')  
        self.DB_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format(self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_NAME)

        setup_db(self.app, self.DB_PATH)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()


        self.Adding_Question = {
            'question' : "What is the currancy of Saudi Arabia ?",
            'answer' : "Ryial",
            'category' : 5,
            'difficulty' : 3
        }
        self.Quiz = { "previous_questions":[],'quiz_category' : {'type': 'History' , 'id' : 4}}

        self.Quiz2 = { "previous_questions":[],'quiz_category' : {'type': 'History' , 'id' : 1}}


    def tearDown(self):
        """Executed after reach test"""
        pass

    """ 14/14
    Q per page [[DONE]]
    Q creat [[DONE]]
    Q delete [[DONE]]
    Category list [[DONE]]
    Q per category [[DONE]]
    Q search [[DONE]]
    Quizzes [[DONE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!]] 

    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    
  # Now for tests 
    ''' Questions per page '''
#Tests for displaying question endpoint 
    # Success test for displaying questions per pages 
    def test_get_paginated_Questions(self):
        res = self.client().get('/Questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['Questions_list'])
        self.assertTrue(data['total_Qs'])

    # Error test for displaying questions for rquested page
    def test_404_sent_requesting_on_unvalid_page(self):
        respond = self.client().get('/Questions?page=2000')
        data = json.loads(respond.data)

        self.assertEqual(respond.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], "resource not found") # the message should be exactly as it is in the errorhandler function





    '''Question addition '''
# Tests for adding new question
    # success request for creating Question
    def test_create_new_Quuestion(self):
        res = self.client().post('/Questions/create', json=self.Adding_Question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['Questions']))

    # Failed on adding Question
    def test_405_when_adding_Question_not_possible(self):
        res = self.client().post('/Questions/create/45', json=self.Adding_Question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')






    '''Question deletion'''
# Tests for delete endpoint 
    # succfull deleting question request 
    # Note \ use new id for each test
    # Tip for using the rest of the tests without this one is to change the function name from test to Test 
    def test_deleting_Question(self):
        res = self.client().delete('/Questions/100')
        data = json.loads(res.data)

        Q = Question.query.filter(Question.id == 10).one_or_none()

        self.assertEqual(Q, None)
        self.assertEqual(res.status_code, 10)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'],10)

    # Deleting non existing question
    def test_deleting_Question_that_does_not_exist(self):
        res = self.client().delete('/Questions/2000')
        data = json.loads(res.data)

        Q = Question.query.filter(Question.id == 2000).one_or_none()
        self.assertEqual(Q, None)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')    







    '''Category list '''
# Tests for Category list endpoint    
    # Success request on getting category list
    def test_get_categories_list(self):
        res = self.client().get('/Questions/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['categories'])        

    # Failed on getting missing categry element 
    def test_error_for_unexisting_category_element(self):
        res = self.client().get('/Questions/categories/0')
        data = json.loads(res.data)

        C = Category.query.filter(Category.id == 0).one_or_none()

        self.assertEqual(C, None)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], 'resource not found')





    '''Qusetions per category  '''
# Tests for category endpoint 
    # Success test for displaying questions for specific Category 
    def test_get_categorized_Questions(self):
        respond = self.client().get('/Categories/1/Questions')
        data = json.loads(respond.data)
        
        self.assertEqual(data['success'],True)
        self.assertEqual(respond.status_code, 200)
        self.assertEqual(data['current_category'],1)
        self.assertTrue(data['total_Qs'])

    # Failed request for displaying questions for unexisting Category 
    def test_error_get_categorized_Questions_unexisting_category(self):
        respond = self.client().get('/Categories/55/Questions')
        data = json.loads(respond.data)
        
        self.assertEqual(data['success'],False)
        self.assertEqual(respond.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')





    '''  Qusetions search'''
# Tests for search results
    # succesful search attempt
    def test_search(self):
        res = self.client().post('/Questions/search', json={'searchTerm': 'what'} )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['Questions'])
        self.assertTrue(data['total_Qs'])
        self.assertTrue(data['current_category'])

    # giving error for specific char
    def test_error_search(self):
        res = self.client().post('/Questions/search', json={'searchTerm': ','} )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')    
        



    '''Quizzes'''
# playing game 
    # checking if post request is succeful
    def test_successful_quizzes(self):

        res = self.client().post('/quizzes', json = self.Quiz)
        data = json.loads(res.data)

       

        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

        self.assertTrue(data['question'])

    # Error for non for non-existing quiz page
    def test_quizzes(self):
        res = self.client().post('/quizzes/3')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
