#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from app import fibo

class FibonacciTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_generator_small(self):
        itr = fibo.generate_seq(4)
        self.assertEqual(next(itr), '0 ')
        self.assertEqual(next(itr), '1 ')
        self.assertEqual(next(itr), '1 ')
        self.assertEqual(next(itr), '2 ')
        self.assertRaises(StopIteration, next, itr)

    def test_large(self):
        fibo_itr = fibo.generate_seq(100)
        for i, val in zip(range(100), fibo_itr):
            if i == 98: self.assertEqual(val, '135301852344706746049 ')
            if i == 99: self.assertEqual(val, '218922995834555169026 ')

if __name__ == '__main__':
    unittest.main()