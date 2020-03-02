from __future__ import division

import os

print(os.getcwd())
print(os.environ["PATH"])
print(os.environ.get("PYTHONPATH"))

import sys

print(sys.executable)

import pyomo
from pyomo.opt import SolverFactory
from pyomo.core import AbstractModel
from pyomo.dataportal.DataPortal import DataPortal
from pyomo import *
import numpy as np
from pyomo.environ import *
# Create abstract model

print('yeeeeeeee')