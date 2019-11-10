import firebase_admin
from firebase_admin import auth
import src.settings
import os
os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
default_app = firebase_admin.initialize_app()

try:
    auth.verify_id_token("ahaha")


from src.app import firebase_app
from firebase_admin import auth
auth.verify_id_token("ahaha")