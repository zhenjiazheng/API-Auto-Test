#!/usr/bin/env python

__author__ = 'zhengandy'
import sys, os


sys.path.extend(os.path.dirname(os.path.abspath(__file__)))
print os.path.dirname(os.path.abspath(__file__))

from argparse import ArgumentParser

ap = ArgumentParser(
    #prog = __file__,
    description = 'xiaowang api unittest',
)

ap.add_argument('number', action="store",type=int, nargs='?', default=-1)

args = ap.parse_args()

import os
os.environ.setdefault('UT_ITEM', str(args.number))

from MileStone4TestCase import testRunner
from MileStone4TestCase import TestCase
testRunner.main()