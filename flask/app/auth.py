from flask import Blueprint, jsonify, make_response, request
from flask.views import MethodView
from mysql.connector import Error
from .db import get_db
from bcrypt import checkpw, gensalt, hashpw
from flask_jwt_extended import create_access_token

register_bp = Blueprint('register', __name__)
login_bp = Blueprint('login', __name__)

class Register(MethodView):
  def post(self):   
    email = request.form['email']
    name = request.form['name']
    password = request.form['password']
    cnx = get_db()
    cur = cnx.cursor()
    error = None
    
    if not email:
      error = 'Email is required'
    elif not name:
      error = 'Name is required'
    elif not password:
      error = 'Password is required'
    
    cur.execute('SELECT id FROM user WHERE email = %s', (email,))
    
    if cur.fetchone() is not None:
      error = f"Email {email} is already registered!"
    
    if error is None:
      query = 'INSERT INTO user (email, name, password) VALUES (%s, %s, %s)'
      hash_password = hashpw(password.encode('utf-8'), gensalt())
      
      cur.execute(query, (email, name, hash_password))
      cnx.commit()
      cur.close()
      
      return make_response(
        jsonify({
          'type': 'success',
          'status': 200,
          'message': 'User addedd successfully'
        })
      )
    else:
      return make_response(
        jsonify({
          'type': 'error',
          'status': 400,
          'message': error
        }), 400
      )

class Login(MethodView):
  def post(self):
    email = request.form.get('email')
    password = request.form.get('password')
    cnx = get_db()
    cur = cnx.cursor()

    if not email:
      return make_response(
        jsonify({
          'type': 'error',
          'status': 400,
          'message': 'Email is required'
        }), 400
      )
    elif not password:
      return make_response(
        jsonify({
          'type': 'error',
          'status': 400,
          'message': 'Password is required'
        }), 400
      )
    
    cur.execute('SELECT * FROM user WHERE email = %s', (email,))
    data = cur.fetchone()
      
    if data is None:
      return make_response(
        jsonify({
          'type': 'error',
          'status': 400,
          'message': 'Incorrect email'
        }), 400
      )
    
    user = extractDataToDictionary(data, cur)
    
    if not checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
      return make_response(
        jsonify({
          'type': 'error',
          'status': 400,
          'message': 'Incorrect password'
        }), 400
      )
    
    # token = encode({'id': user['id']}, getenv("SECRET_KEY"), algorithm="HS256")
    token = create_access_token(identity={'id': user['id'], 'email': user['email']})
    return make_response(
      jsonify({
        'type': 'success',
        'status': 200,
        'message': 'Login success',
        'token': token
      })
    )
      
register_view = Register.as_view('register')
register_bp.add_url_rule('/register/', view_func=register_view)

login_view = Login.as_view('login')
login_bp.add_url_rule('/login/', view_func=login_view)

def extractDataToDictionary(data, cursor):
  """merge row and data to be dictionary

  Args:
      data (tuple): tuple of data, ex: (1, 'budi', '1234')
      cursor (cursor()): get every row ex: ('id', 'name', 'password') from the last fetch

  Returns:
      data: data as dictionary ex: {'id': 1, 'name': 'budi', 'password': '1234'}
  """  
  row = [x[0] for x in cursor.description]
  user = {}
  
  for i in range(len(data)):
    user[row[i]] = data[i]
  
  return user