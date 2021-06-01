import os
from mysql.connector import connect, Error, errorcode
from bcrypt import hashpw, gensalt
from operator import itemgetter
from uuid import uuid4

USER = os.getenv('MYSQL_USER') if os.getenv('MYSQL_USER') else 'root'
HOST =os.getenv('MYSQL_HOST') if os.getenv('MYSQL_HOST') else '127.0.0.1'

config = {
  'user': USER,
  'password': '',
  'host': HOST,
  'port': 3306,
}

def get_db():
  """Start connection to database

  Returns:
      cnx: connect() object
  """  
  try:
    config['database'] = 'bookmark'
    config['pool_name'] = 'bookmark_pool'
    config['pool_size'] = 20
    cnx = connect(**config)
    return cnx
  except Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print('Username or password is invalid')
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print('Database doesn\'t exist')
    else:
      print(err)
    

def init_db():
  """Initialize the database"""  
  
  cnx = connect(**config)
  cur = cnx.cursor()
  
  # Create Bookmark Database
  cur.execute('DROP DATABASE IF EXISTS bookmark')
  cur.execute('CREATE DATABASE bookmark')
  cur.close()
  
  cnx = get_db()
  cur = cnx.cursor()
  
  # Create User Table
  cur.execute('DROP TABLE IF EXISTS user')
  cur.execute('CREATE TABLE user (id VARCHAR(50) PRIMARY KEY, email VARCHAR(100) NOT NULL,name VARCHAR(100) NOT NULL, password VARCHAR(255) NOT NULL)')
  cnx.commit()
  
  # Create Bookmark Table
  cur.execute('DROP TABLE IF EXISTS bookmark')
  cur.execute('CREATE TABLE bookmark (id VARCHAR(50) PRIMARY KEY, author_id VARCHAR(50) NOT NULL, created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, title VARCHAR(255) NOT NULL, url VARCHAR(255) NOT NULL, img VARCHAR(255) NULL, description VARCHAR(255) NULL, FOREIGN KEY (author_id) REFERENCES user (id))')
  cnx.commit()
  
  cur.close()
  cnx.close()
  
  print('Initialized the database')
  
def seed():
  """Seed the database"""
  hash_password = hashpw("tabi".encode('utf-8'), gensalt())
  user_id = str(uuid4())
  users = [{ 'id': user_id, 'email': 'tabi@gmail.com', 'name': 'tabi', 'password': hash_password }]
  bookmarks = [
    {
      'id': str(uuid4()),
      'author_id': user_id,
      'title': 'Atomic Habits',
      'url': 'example.com',
      'img': 'https://i.redd.it/fyqoq0jzoht21.jpg',
      'description': 'Perubahan kecil yang memberikan hasil luar biasa'},
    {
      'id': str(uuid4()),
      'author_id': user_id,
      'title': 'Sebuah Seni Untuk Bersikap Bodo Amat',
      'url': 'example.com',
      'img': 'https://i.redd.it/fyqoq0jzoht21.jpg',
      'description': 'Cara mudah dan terbukti untuk bersikap bodo amat'},
    ]
  cnx = get_db()
  cur = cnx.cursor()
  
  
  # Seed User Table
  for user in users:
    id, email, name, password = itemgetter('id', 'email', 'name', 'password')(user)
    
    query = "INSERT INTO user(id, email, name, password) VALUES(%s, %s, %s, %s)"
    cur.execute(query, (id, email, name, password))
    cnx.commit()
    
  print('Insert into table user success!')
  
  # Seed Bookmark Table
  for bookmark in bookmarks:
    bookmark_id, title, url, img, description = itemgetter('id', 'title', 'url', 'img', 'description')(bookmark)
    query = "INSERT INTO bookmark(id, author_id, title, url, img, description) VALUES(%s, %s, %s, %s, %s, %s)"
    cur.execute(query, (bookmark_id, user_id, title, url, img, description))
    cnx.commit()
  
  print('Insert into table bookmark success!')
  
  cur.close()
  cnx.close()
  
  print("Database seeded")       
    