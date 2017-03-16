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

## Implementation Considerations
Here is what I thought about when implementing this service at first.
1. Streaming sequence response. Streaming is always best practice for large size of response, although in this demo the response size is only ~1MB and works even without streaming. 
2. Flask itself is not running in concurrent way. When deploy this in production environment, Gunicorn (or other WSGI server) is required to support multiple users.
3. Why has maxinum input number: I tried with 100,000 as input and it took ~15 minutes to return. See the section of [Performance](#performance) for further analysis. I also have some thoughts on performance improvement, see [More Ideas](#more-ideas). For now let me leave this simple implementation with the limitation of max input number to 10, 000. 

## Performance
The test below indicates that the convertion from big num to string is the major time consumer. Here is the code for testing:
```python
def generate_seq(sn):
    """To stream fibo sequence returned """
    a, b = 0, 1
    for i in range(sn):
        yield to_str(a)
        a, b = b, a+b

def to_str(n):
    return str(n) + ' '  # this is the performance killer

if __name__ == '__main__':
    import cProfile
    cProfile.run('for n in generate_seq(100000): pass')
```
Here is what I found
1. This program with 100,000 as input took more than 10 minutes to finish. It's 1.45 seconds when I comments out the line of convertion.
2. to_str() takes most of time (from output of cProfile and 10,000 as input):
```
      20004 function calls in 1.114 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.002    0.002    1.114    1.114 <string>:1(<module>)
    10000    1.094    0.000    1.094    0.000 test.py:26(to_str)        ##### to_str takes most of time 
    10001    0.018    0.000    1.112    0.000 test.py:4(generate_seq)
        1    0.000    0.000    1.114    1.114 {built-in method exec}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}```
```

3. 0.031 seconds is taken for converting the fibonacci value of 100,000th number to a string:
```
         4 function calls in 0.031 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.031    0.031 <string>:1(<module>)
        1    0.031    0.031    0.031    0.031 test.py:26(to_str)    ##############
        1    0.000    0.000    0.031    0.031 {built-in method exec}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
```

According to the observation above, the bad performance comes from the conversion from bigint to string. If we can cache the fibonacci value or sequence somewhere as string, it will help on performance. Discuss this on the section of [More Ideas](#more-ideas) 


## More Ideas
