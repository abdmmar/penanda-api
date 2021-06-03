from operator import ge
from flask import Blueprint, jsonify, request, make_response
from flask.views import MethodView
from mysql.connector import Error
from flask_jwt_extended import jwt_required, get_jwt_identity
from metadata_parser import MetadataParser
from shortuuid import uuid

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
        cnx.close()
        
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
        
        cur.close()
        cnx.close()
        
        return make_response(
          jsonify({
            'type': 'success',
            'status': 200,
            'message': 'Bookmark found',
            'result': bookmark
          })
        )

  def post(self):
    """Add bookmark metadata from url to database

    Returns:
        JSON: {type, status, message}
    """       
    url = request.form.get('url')
    user = get_jwt_identity()
    user_id = user.get('id')
    
    if not url:
      return make_response(
        jsonify({
          'type': 'error', 
          'status': 400, 
          'message': 'Url is required!'
          }), 400
        )
    
    page = MetadataParser(url=url,force_doctype=True, search_head_only=False, support_malformed=True)
    title = page.get_metadatas('title', strategy=['page', 'meta', 'og', 'twitter', 'dc'])[0] # ['string']
    img = page.get_metadata_link('image', allow_encoded_uri=True) # Return a 'string'
    description = page.get_metadatas('description')[0][0:254] # Returned a list ['string'] and trim max 255 char
    type = page.get_metadatas('type')[0] # Returend a list ['string']
    
    if title is None:
      title = ''
    elif img is None:
      img = ''
    elif description is None:
      description = ''
    
    cnx = get_db()
    cur = cnx.cursor()
    
    try:
      bookmark_id = str(uuid()[:-6])
      query = 'INSERT INTO bookmark(id, author_id, title, url, img, description) VALUES (%s,%s,%s,%s,%s,%s)'
      cur.execute(query, (bookmark_id, user_id, title, url, img, description))
    except Error as err:
      print(err)
      
      return make_response(
      jsonify({
        'type': 'error', 
        'status': 500, 
        'message': 'Internal server error, add bookmark failed!'
        }), 500
      )
      
    cnx.commit()
    cur.close()
    cnx.close()
    
    return make_response(
      jsonify({
        'type': 'success', 
        'status': 200, 
        'message': 'Bookmark added succesfully!'
        }), 200
      )

  def delete(self, bookmark_id):
    if bookmark_id is None:
      return make_response(
        jsonify({
        'type': 'error', 
        'status': 400, 
        'message': 'Id is required!'   
        }), 400
      )
      
    cnx = get_db()
    cur = cnx.cursor()

    try:
      query="DELETE FROM bookmark WHERE id = %s"
      cur.execute(query, (bookmark_id,))
    except Error as err:
      print(err)
      
      return make_response(
      jsonify({
        'type': 'error', 
        'status': 500, 
        'message': 'Internal server error, delete bookmark failed!'
        }), 500
      )
    
    cnx.commit()
    cur.close()
    cnx.close()
    
    return make_response(
      jsonify({
        'type': 'success', 
        'status': 200, 
        'message': 'Bookmark deleted succesfully!'
      }), 200
    )

  def put(self, bookmark_id):
    if bookmark_id is None:
      return make_response(
        jsonify({
        'type': 'error', 
        'status': 400, 
        'message': 'Bookmark ID is required!'   
        }), 400
      )
      
    title = request.form.get('title')
    url = request.form.get('url')
    img = request.form.get('img')
    description = request.form.get('description')
    
    # TODO: Add URL Validation
    
    if url == '':
      return make_response(
        jsonify({
          'type': 'error', 
          'status': 400, 
          'message': 'URL can\'t be empty otherwise you shouldn\'t change it'
        }), 400
      )
      
    update_item = {'title': title, 'url': url, 'img': img, 'description': description}
    query_set_item_list = []
    query_set = ' '
    
    for keys, item in update_item.items():
      if item is not None:
        query_set += f'{keys}=%s, '
        query_set_item_list.append(item)
    
    query_set_item_list.append(bookmark_id)
    query_set_item = tuple(query_set_item_list)
    
    cnx = get_db()
    cur = cnx.cursor()
    
    try:
      query = "UPDATE bookmark SET " + query_set[:-2] + " WHERE id=%s"
      cur.execute(query, query_set_item)
    except Error as err:
      print(err)
      
      return make_response(
      jsonify({
        'type': 'error', 
        'status': 500, 
        'message': 'Internal server error, update bookmark failed!'
        }), 500
      )
    
    cnx.commit()
    cur.close()
    cnx.close()
    
    return make_response(
      jsonify({
        'type': 'success', 
        'status': 200, 
        'message': 'Bookmark updated succesfully!'
      }), 200
    )

register_api(bp, Bookmark, "bookmark", "/bookmark/", "bookmark_id", "string")

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