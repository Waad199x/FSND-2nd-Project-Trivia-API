import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

# 10/10 TODOs


QUESTIONS_PER_PAGE = 10

def paginate_Qs(request, selection):
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  Questions = [Q.format() for Q in selection]  
  current_page = Questions[start:end]
  
  return current_page

    
  '''
  @TODO: [[DONE]] Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


  '''
  @TODO: [[DONE]] Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
      return response

  def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct  



  '''
  @TODO: [[DONE]]
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  # since catecories needed in more than one page in this project so i see making seperate function to generate them is better

  def all_catecories():
    category = Category.query.all()
    categories_list = []
    for a in category :
        categories_list.append(a.id)
        categories_list.append(a.type)
    categories_dict= Convert(categories_list)
    return categories_dict


  @app.route('/Questions/categories')
  def catecories_list():
    if len(all_catecories()) == 0:
      abort(404)
 
    return jsonify({
      'success': True,
      'categories' : all_catecories()

      })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/Questions')
  def retrieve_Questions():
    #ordering by newest added
    selection = Question.query.order_by(Question.id).all()
    current_page = paginate_Qs(request, selection)
    
    if len(current_page) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'Questions_list': current_page,
      'total_Qs': len(Question.query.all()),
      'categories' : all_catecories(),
      'current_category': all_catecories()
      })

# may i make a new site url that takes the get req foe category and display that current category only 

  '''
  @TODO: [[DONE]]
  Create an endpoint to DELETE question using a question ID.  

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/Questions/<int:Q_id>', methods=['DELETE'])
  def delete_Q(Q_id):
    #curl -X DELETE http://127.0.0.1:5000/Questions/(id)

    try:
      Q = Question.query.filter(Question.id == Q_id).one_or_none()
      Q.delete()

      if Q is None:
        abort(404)

      return jsonify({
        'success': True,
        'deleted': Q_id
      })

    except:
      abort(422)




  '''
  @TODO: [[DONE]]
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/Questions/create', methods=['POST'])
  def post_Question():
    #curl -X POST -H 'Content-Type: application/json' http://127.0.0.1:5000/Questions/create -d '{"question":"Neverwhere", "answer":"Neil Gaiman","category":"5", "difficulty":"5"}' 
    #Correct curl request - >  curl -X POST -H 'Content-Type:application/json' http://127.0.0.1:5000/Questions/create -d '{"question":"What ..?","answer":"Answer","category":"5","difficulty":"5"}'
    # curl http://127.0.0.1:5000/Questions/create -X POST  -H 'Content-Type:application/json'  -d '{"question":"What ..?","answer":"Answer","category":"5","difficulty":"5"}' 
        body = request.get_json()
        new_question = body.get('question',None)
        new_answer = body.get('answer',None)
        new_category = body.get('category',None)
        new_difficulty = body.get('difficulty',None)   

        try:
            new_Q = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
            new_Q.insert()
            selection = Question.query.order_by(Question.id).all()
            current_page = paginate_Qs(request, selection)

            return jsonify({
              'success': True,
              'created': new_Q.id,
              'Questions': current_page,
              'total_Qs': len(Question.query.all())
            })

        except:
          abort(422)


  '''
  @TODO: [[DONE]]
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/Questions/search', methods=['POST'])
  def search_Question():

    body = request.get_json()
    searchTerm = body.get('searchTerm', None)   

    try:
      search_results = Question.query.order_by(Question.category).filter(Question.question.ilike('%{}%'.format(searchTerm)))
      current_page = paginate_Qs(request, search_results)
      
      return jsonify({
          'success': True,
          'Questions': current_page,
          'total_Qs': len(search_results.all()),
          'current_category' : all_catecories()
        })
     
    except:
       abort(422)


  '''
  @TODO: [[DONE]]
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/Categories/<int:Category_id>/Questions')
  def Questions_by_category(Category_id):
    
    Questions_by_category = Question.query.order_by(Question.id).filter(Question.category == Category_id).all()
    current_page = paginate_Qs(request, Questions_by_category)

    if len(current_page) == 0:
      abort(404)


    return jsonify({
      'success': True,
      'Questions_list': current_page,
      'current_category': Category_id,
      'total_Qs': len(Questions_by_category)
      })







  '''
  @TODO:  [[DONE]]
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/quizzes', methods=['POST'])
  def Play_Question():

    try:
      body = request.get_json()
      previous_questions = body.get("previous_questions")
      quiz_category = body.get('quiz_category')

      if quiz_category['type'] == 'click':
        Quiz_Questions = Question.query.filter(Question.id.notin_((previous_questions))).all()
      else :         
        Quiz_Questions = Question.query.filter(Question.id.notin_((previous_questions))).filter_by(category = quiz_category['id'] ).all()

      #Using the python built in function random() to get a random Question from the Quiz_Questions list
      random_index = int(random.random() * len(Quiz_Questions))
      if len(Quiz_Questions) > 0:
        Random_Question = Quiz_Questions[random_index].format() 
      else: None

      return jsonify({
              'success': True,
              'question': Random_Question
            })
    except :
      abort(422)


  '''
  @TODO: [[DONE]]
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(404)
  def not_found(error): #usualy when there is a problem in the url
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
      }), 404

 
  @app.errorhandler(422)
  def unprocessable(error): 
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400
  return app

    
