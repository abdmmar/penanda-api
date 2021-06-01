from flask import Blueprint, jsonify, request, make_response
from flask.views import MethodView
from mysql.connector import Error
from flask_jwt_extended import jwt_required, get_jwt_identity
from .util import register_api, extractDataToDictionary
from .db import get_db

ID = 4
# It's should use Map lol
FAKE_DATA = [{"user_id": 3, "name": "duck"}, {"user_id": 2, "name": "cat"}]

bp = Blueprint("bookmark_api", __name__)

class Bookmark(MethodView):
  decorators = [jwt_required()]
  
  def get(self, bookmark_id):
    """ Get bookmark list from database"""
    if bookmark_id is None:
        user = get_jwt_identity()
        
        cnx = get_db()
        cur = cnx.cursor()
        
        try:
          query = "SELECT * FROM bookmark"
          cur.execute(query)
        except Error as err:
          print(err)
        
        data = cur.fetchall()
        bookmarks = convertListOfTuplesToArrayOfDictionary(data, cur)
        
        cur.close()
        
        return jsonify({'result': bookmarks})
    else:
        cnx = get_db()
        cur = cnx.cursor()
        
        try:
          query = "SELECT * FROM bookmark WHERE id = %s"
          cur.execute(query, (bookmark_id,))
        except Error as err:
          print(err)
        
        data = cur.fetchone()
        
        if data is None:
          return make_response(
            jsonify({
              'type': 'error',
              'status': 400,
              'message': 'Bookmark not found'
            }), 400
          )
          
        bookmark = extractDataToDictionary(data, cur)
        
        return make_response(
          jsonify({
            'type': 'success',
            'status': 200,
            'message': 'Bookmark found',
            'result': bookmark
          })
        )

  def post(self):
    """Add bookmark url to database

    Returns:
        JSON: {type, status, message}
    """       
    url = request.form.get('url')
    data = {'user_id': ++ID, "name": url}
    
    if not url:
      return make_response(
        jsonify({
          'type': 'error', 
          'status': 400, 
          'message': 'Name is required!'
          }), 400
        )
    
    FAKE_DATA.append(data)
    
    return make_response(
      jsonify({
        'type': 'success', 
        'status': 200, 
        'message': 'User added succesfully!'
        })
      )

  def delete(self, user_id):
    if user_id is None:
      return make_response(
        jsonify({
        'type': 'error', 
        'status': 400, 
        'message': 'Id is required!'   
        }), 400
      )
    elif type(user_id) is not int:
      return make_response(
        jsonify({
        'type': 'error', 
        'status': 400, 
        'message': 'Id must be number!'   
        }), 400
      )
    
    res = {
      'type' : 'error',
      'status' : 400,
      'message' : 'User deleted failed!'
    }
    
    for index, data in enumerate(FAKE_DATA, 0):
      if data['user_id'] == user_id:
        FAKE_DATA.pop(index)
        res['type'] = 'success'
        res['status'] = 200
        res['message'] = 'User deleted successfully!'
    
    return make_response(jsonify(res), res.get('status'))

  def put(self, user_id):
    name = request.form['name']
    
    if len(name) == 0:
      return make_response(
        jsonify({
          'type': 'error', 
          'status': 400, 
          'message': 'Name is required!'
          }), 400
        )
    
    if user_id is None:
      return make_response(
        jsonify({
        'type': 'error', 
        'status': 400, 
        'message': 'Id is required!'   
        }), 400
      )
    elif type(user_id) is not int:
      return make_response(
        jsonify({
        'type': 'error', 
        'status': 400, 
        'message': 'Id must be number!'   
        }), 400
      )
    
    res = {
      'type' : 'error',
      'status' : 400,
      'message' : 'User updated failed!'
    }
    
    for data in FAKE_DATA:
      if data['user_id'] == user_id:
        data['name'] = name
        
        res['type'] = 'success'
        res['status'] = 200
        res['message'] = 'User updated successfully!'
    
    return make_response(jsonify(res), res.get('status'))

register_api(bp, Bookmark, "bookmark", "/bookmark/", "bookmark_id")

def convertListOfTuplesToArrayOfDictionary(list_of_data, cursor):
  """Convert list of tuples to array of dictionary so it can be send as JSON properply

  Args:
      list_of_data (tuple): (('tuple'), ('tuple2'))
      cursor (object): cursor() object

  Returns:
      dictionary: return data as dictionary
  """  
  row_headers=[x[0] for x in cursor.description]
  data = []
  
  for bookmark in list_of_data:
    data.append(dict(zip(row_headers, bookmark)))
    
  return data