#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from app import fibo


class FiboTestCase(unittest.TestCase):
    def setUp(self):
        self._fibo_client = fibo.fibo_app.test_client()

    def test_fib_not_a_number(self):
        rv = self._fibo_client.get('/?sn=ab')
        self.assertTrue(rv.status.startswith('400 '))

    def test_fib_float_number(self):
        rv = self._fibo_client.get('/?sn=1.0')
        self.assertTrue(rv.status.startswith('400 '))

    def test_fib_negative_numer(self):
        rv = self._fibo_client.get('/?sn=-1')
        self.assertTrue(rv.status.startswith('400 '))

    def test_fib_overflowed_number(self):
        rv = self._fibo_client.get('/?sn=99999999999999')
        self.assertTrue(rv.status.startswith('400 '))

    def test_fib_zero(self):
        rv = self._fibo_client.get('/?sn=0')
        self.assertTrue(rv.status.startswith('200 '))
        self.assertEqual(rv.data, b'')

    def test_fib_normal(self):
        rv = self._fibo_client.get('/?sn=5')
        self.assertTrue(rv.status.startswith('200 '))
        self.assertEqual(rv.data, b'0 1 1 2 3 ')


        rv = self._fibo_client.get('/?sn=10')
        self.assertTrue(rv.status.startswith('200 '))
        self.assertEqual(rv.data, b'0 1 1 2 3 5 8 13 21 34 ')

if __name__ == '__main__':
    unittest.main()