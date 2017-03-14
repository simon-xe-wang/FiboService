#!venv/Scripts/python
import os
from app import fibo_app
fibo_app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8888)))