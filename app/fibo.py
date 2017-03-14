#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A RESTful web service that provides the sequence of Fibonacci numbers for
 given integer less than a predefined number
"""

from app import fibo_app
from flask import request
from flask import abort
from flask import Response

MAX_SN = 10000

@fibo_app.route('/')
def index():
    """The REST API which accepts input number and returns fibonacci sequence

        To get a sequence user need to input https://myfibo.herokuapp.com/?sn=10
        Query parameter sn indicates how many numbers should have in returned sequence
    """
    sn = request.args.get('sn')
    if not sn:
        abort(400, "SN is required. Try https://myfibo.herokuapp.com/?sn=<number>")
    try:
        sn = int(sn)
        if sn < 0 or sn > MAX_SN:
            abort(400, "SN must be 0 - {}".format(MAX_SN))
    except ValueError:
        abort(400, "Invalid SN. It must be an integer.")

    return Response(generate_seq(sn))

def generate_seq(sn):
    """To stream fibo sequence returned """
    a, b = 0, 1
    for i in range(sn):
        yield str(a) + ' '
        a, b = b, a+b

def build_seq(sn):
    """Return fibo sequence as a list. """
    seq = []
    a, b = 0, 1
    for i in range(sn):
        seq.append(str(a))
        a, b = b, a+b
    return seq

if __name__ == '__main__': # for profiling where is the time consumer.
    import cProfile
    cProfile.run('for n in fibo.generate_seq(10000): pass')

