from app import fiboApp
from flask import request
from flask import abort
from flask import Response
import cProfile

@fiboApp.route('/fibo')
def index():
    sn = request.args.get('sn')
    if not sn:
        abort(400, "SN in query parameter is required")

    return Response(generate_seq(int(sn)))

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


