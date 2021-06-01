from os import getenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Config():
  """Configuration for application factory
  """
  JWT_SECRET_KEY = getenv('SECRET_KEY')

class TestingConfig():
  JWT_SECRET_KEY = getenv('SECRET_KEY')
  