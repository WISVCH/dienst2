from django.utils import unittest
from kas.models import *

class TransactionsTestCase(unittest.TestCase):
  def setUp(self):
    print "Setup "

  def test_transaction_1(self):
    """Create a transaction"""
    