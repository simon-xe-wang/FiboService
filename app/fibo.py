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

MAX_SN = 100000

# Cache to hold the string of each fibo value
_fibo_list = ['0', '1']

@fibo_app.route('/')
def index():
    """
    The REST API which accepts input number and returns fibonacci sequence

    To get a sequence user need to input https://myfibo.herokuapp.com/?sn=10
    Query parameter sn indicates how many numbers should have in returned sequence
    """
    sn = request.args.get('sn')
    if not sn:
        abort(400, "SN is required, e.g. https://myfibo.herokuapp.com/?sn=<number>")
    try:
        sn = int(sn)
        if sn < 0 or sn > MAX_SN:
            abort(400, "SN must be 0 - {}".format(MAX_SN))
    except ValueError:
        abort(400, "Invalid SN. It must be an integer.")

    return Response(_generate_seq2(sn))

def _generate_seq(sn):
    """
    The generate which generate the string of each fibo value directly
    """
    a, b = 0, 1
    for i in range(sn):
        yield str(a) + ' '
        a, b = b, a+b

def _generate_seq2(sn):
    """
    Another generator which uses cache to generate the string of each fibo value.
    Fill cache first if the values are not in.
    :param sn:
    :return:
    """
    if sn > len(_fibo_list):
        _fill_cache(sn)

    for val in range(sn):
        yield _fibo_list[val] + ' '

def _fill_cache(sn):
    '''
    Fill cache with fibo strings from current length to sn
    :param sn:
    :return:
    '''
    a = int(_fibo_list[len(_fibo_list)-2])
    b = int(_fibo_list[len(_fibo_list)-1])
    for i in range(len(_fibo_list), sn):
        a, b = b, a+b
        _fibo_list.append(str(b))

def _clear_cache():
    """
    For testing purpose
    :return:
    """
    _fibo_list.clear()
    _fibo_list.append('0')
    _fibo_list.append('1')
