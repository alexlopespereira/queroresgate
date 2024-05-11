import os


DEBUG = os.environ.get('DEBUG') == "True"
SIDE = os.environ.get('SIDE') or 0.02
VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'
