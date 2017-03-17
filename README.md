# FiboService
## About
FiboService is a RESTful Web Service which provides Fibonacci sequence for given input number (start from 0). For now the max input is 100,000 for demo purpose. 

Demo is available on Heroku for demo: https://myfibo.herokuapp.com/?sn=10. Its max input is 10, 000 as the host only has 512MB memory (Note: you might see a delay for the first request as it falls into sleep after 30 minutes idle time)

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
Note: if input a large number like 100,000 for the first time, it's going to take 20 minutes to return. The time is spent on filling cache and the following requests will be fast (less than 10 seconds). 

## Implementation Considerations
Flask built-in server works in single process mode. What I implemented here is only applicapable for single process. We will discuss multi process and distributed solution in [More Ideas](#more ideas)

The first version I did is very simple. I used a generator to generate each fibonacci value string and Flask send each one as response in streaming way. This works well for small input number like 10,000. When I tried 100,000. It took about 20 minutes, too bad!

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

Again, it's the conversion from bigint to string has bad performance and I don't find a good way to optimize it.

Then I wrote version 2 which caches the fibonacci value string in a list. Assuming the maximum amount is 100, 000, which takes around over 1GB memory. It looks like
```
fibo_list: ['0', '1', '1', '2', '3', '5', ...]
```

Everytime getting a request with input number, get each string from the cache directly and return to client until reaching input value. If required values are not in cache, populate them. 

The first request of asking big number like 100,000 is still very slow but the following will be fast. 

This works well for single process. The cons is:
1. Not work for multiple processes we need to put this into shared memory. 
2. It uses much memory

This is what I implemented for now. There are other ways which might work bette in distributed environment and we will discuss it next. 

## More Ideas

Another way is caching the stream of sequence into disk and build a index table in memory. The idea is creating one or more files on disk to save the fibo sequence in order, and creating an index table in memory which indicates the file and the offset for each number, which looks like:
```
file1:  0 1 1 2 3 5 8 13 21 34 55 89 ...        # separated by ' ' 

Index table {0: 1, 1:2, 2: 4, 3: <offset>, ... }
```
This way we can read file from the begining to the offset for input number directly. So no need to hold all data in memory. The index table is much smaller. For example, holding 1M entries takes around 16MB (16 bytes*1M). 

The performance of this should be fine, specially when the network bandwidth between user and server is lower than disk bandwidth. 

Both ways would help on performance. To extend that to multiple processes and multiple hosts environment, there are the following questions to think about:

(The questions below are for the way of caching data on disk, though fit for cache in memory)

For multiple processes:

1. The data file can be shared across processes, but index table can't. Shall we use multiprocessing.Manager to store index table ?  

For multiple hosts:

2. The length of each fibo value is variable, how we split data into servers evenly? 
3. How an API server knows which storage server should go to get data. 
4. One server storing particular range of data might become hotspot, how to resolve. 
5. The cache on disk could be pre populated or dynamically on demand. Which one is better? 

