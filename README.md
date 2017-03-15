# FiboService
## About
FiboService is a RESTful Web Service which provides Fibonacci sequence for given input number (start from 0). For now the max input is 10,000 for demo purpose. 

Demo is available on Heroku for demo: https://myfibo.herokuapp.com/?sn=10 (Note: you might see a delay for the first request as it falls into sleep after 30 minutes idle time)

## Prerequisites and Run

If you would like to install this service locally, Python 3+ and [Flask (0.1.2)](http://flask.pocoo.org/docs/0.12/installation/) are required. You might also want to use [virtualenv](https://virtualenv.pypa.io/en/stable/installation/) to setup an isolated environment.

Run FiboService locally is simple:
```
# python run.py
```
This will start service at 0.0.0.0:8888.

You can use browswer or curl as client for try:
```
# curl -k https://myfibo.herokuapp.com/?sn=20
```

## Implementation Consideration
## Test
## Performance
## Future Works
