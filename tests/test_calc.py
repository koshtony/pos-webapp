import unittest
from pambo.calc import numProd,profSum,expSum
from pambo.database import products,sales,expenses
class TestCalculations(unittest.TestCase):
    # test summation of products quantity
    def test_numProd(self):
        #self.assertEquals(numProd([{}]),0)
        self.assertEquals(numProd(products.query.all()),3)
    # test profit and price results
    def test_profSum(self):
        prof,_=profSum(sales.query.all())
        self.assertEquals(prof,500)
    # test expenses results
    def test_expSum(self):
        self.assertEquals(expSum(expenses.query.all()),0)