from cryptography.fernet import Fernet
from .credentials import pass_key
  
key = pass_key #your key goes here
  
KEY = Fernet(key)