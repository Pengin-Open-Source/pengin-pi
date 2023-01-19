import os
from flask import request, jsonify
from functools import wraps
from requests import post
from dotenv import load_dotenv
load_dotenv()


VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"
secret_key = os.getenv("SECRET_KEY")

#secret_key = os.getenv("SECRET_KEY")
def verify_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = request.form.get('g-recaptcha-response')
        g_response = post(url=f'{VERIFY_URL}?secret={secret_key}&response={response}').json()
        if not g_response["success"] or g_response["score"] < 0.6:
            return jsonify({"error": "human verification failed"}), 403
        
        return func(*args, **kwargs)
    return wrapper
    # "verify_response" example: {'success': True, 'challenge_ts': '2023-01-10T03:01:06Z', 'hostname': 'localhost', 'score': 0.9, 'action': 'submit'}

