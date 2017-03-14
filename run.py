#!venv/Scripts/python
import os
from app import fiboApp
fiboApp.run(host='0.0.0.0', port=os.getenv('PORT', 8888) )