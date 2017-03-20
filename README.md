# FiboService
## About
FiboService is a RESTful Web Service which provides Fibonacci sequence (start from 0) for given input number. For now the valid input range is 0 to 100,000. 

Demo is available on Heroku: https://myfibo.herokuapp.com/?sn=10. The max input is 10, 000 as the host only has 512MB memory (Note: you might see a delay for the first request as it falls into sleep after 30 minutes idle time)

## Prerequisites and Run

If you would like to run this service locally, Python 3.4+ and [Flask (0.1.2)](http://flask.pocoo.org/docs/0.12/installation/) are required. 
```
# pip install flask
```
You might also want to use [virtualenv](https://virtualenv.pypa.io/en/stable/installation/) to setup an isolated environment.

Run FiboService locally is simple:
```
# python run.py
```
This will start service at 0.0.0.0:8888.

You can use browswer or curl as client for try:
```
# curl -k http://127.0.0.1:8888/?sn=20
```

Note: The first request with large number like 100,000 is going to take 20 minutes to return. The time is spent on filling cache and the following requests will be fast (less than 10 seconds). 

## Requirements
The web service accepts a number, n, as input and returns the first n Fibonacci numbers, starting from 0. I.e. given n = 5, appropriate output would represent the sequence "0 1 1 2 3".
Given a negative number, float or any non-numeric, it will respond with "400 Bad Request" and Error message

## Implementation Considerations
Flask development server works in single process mode. What I implemented here is only applicapable for single process. We will discuss multi process and distributed solution in [More Ideas](#more ideas)

The first version I did is simple. I used a generator to generate each fibonacci value string and Flask sends each one in streaming way. This works well for small input number like 10,000. When I tried 100,000. It took about 20 minutes. 

The tests below indicates the conversion from bignum to int is the performance killer:

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
1. This program with 100,000 as input took more than 20 minutes to finish while it was 1.45 seconds when repalced the line with just returning number.
2. to_str() takes most of time (from output of cProfile and 10,000 as input):

```
      20004 function calls in 1.114 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.002    0.002    1.114    1.114 <string>:1(<module>)
    10000    1.094    0.000    1.094    0.000 test.py:26(to_str)        ##### to_str takes 99% of time 
    10001    0.018    0.000    1.112    0.000 test.py:4(generate_seq)
        1    0.000    0.000    1.114    1.114 {built-in method exec}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}```
```

3. 0.031 seconds is taken for converting the fibonacci value of 100,000th number to a string. (0.03*100000 = 3000 seconds):
```
         4 function calls in 0.031 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.031    0.031 <string>:1(<module>)
        1    0.031    0.031    0.031    0.031 test.py:26(to_str)    ##############
        1    0.000    0.000    0.031    0.031 {built-in method exec}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
```

Again, it's the conversion from bigint to string has bad performance and I don't find a good way to optimize it.

Then I wrote version 2 which caches the fibonacci value string in a list. Assuming the maximum amount is 100, 000, which takes around over 1GB memory. It looks like
```
fibo_list: ['0', '1', '1', '2', '3', '5', ...]
```

Every time getting a request with input number, starting from 0, get corresponding string for each number from the cache and write to response in streaming way until reaching the input value. If required values are not in cache, populate them before return. 

Since this is only single process so lock is not required. It's needed when supporting multiple user.

The first request of asking big number like 100,000 is still very slow (20 minutes) but the followings will be fast (6 seconds). 

This works well for single process. The drawbacks are:
1. Cache locates within a process. Need to share with others.  
2. Large memory usage might be an issue.

This is what I implemented for now. There are other ways which might work better in distributed environment and we will discuss it next. 

## More Ideas

Another way is caching the stream of sequence into disk and build a index table in memory. The idea is creating one or more files on disk to save the fibo sequence in order, and creating an index table in memory which indicates the file and the offset for each number, which looks like:
```
file1:  0 1 1 2 3 5 8 13 21 34 55 89 ...        # separated by ' ' 

Index table: [offset1 for 0, offset2 for 1, ..., offsetn for number n]
```
This way we can read file from the begining to the offset for input number directly. So no need to hold all data in memory. The index table takes much less memory. For example, holding 1M entries takes around 16MB 
'''
(8 bytes for key + 8 bytes for offset) * 1 million = 16MB 
'''

The performance of this should be fine, specially when the network bandwidth between client and server is lower than disk bandwidth. 

Both ways would help on performance. To extend that to multiple processes and multiple hosts environment, there are the following questions to think about:

For multiple processes:

1. The data file on disk can be shared across processes. Need to find a way (multiprocessing.Array?) to hold index table and share across processes.  

For multiple hosts:
Suppose need to support very big fibo sequence (say sn = 1,000, 000, 000) and single host can't deal with that alone. 
1. How should we partition sequence evenly to multiple hosts? 
2. What index table would look like? 
4. For each range, need replication for load balancing and failure tolerence. 
5. What will happen if need to rebuild one or all ranges. (Impact on index table)
6. Could a range be a hotspot and how to resolve it? 
7. Pre populate cache vs fill on demand? 

