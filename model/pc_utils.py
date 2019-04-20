#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
pc_utils

simple data loader module. Loads data files from the "data" directory shipped with application.
Enhancing this to handle caching etc.

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import os
import sys

# < module data >----------------------------------------------------------------------------------

# data
M_DATA_PY = os.path.abspath(os.path.dirname(__file__))
M_DATA_DIR = os.path.normpath(os.path.join(M_DATA_PY, "../.."))

# -------------------------------------------------------------------------------------------------
def filepath(f_filename):
    """
    determine the path to a file in the data directory
    """
    # return
    return os.path.join(M_DATA_DIR, f_filename)

# -------------------------------------------------------------------------------------------------
def load(f_filename, f_mode="rb"):
    """
    open a file in the data directory
    """
    # return
    return open(os.path.join(M_DATA_DIR, f_filename), f_mode)

#===============================================================================
# partial: very useful function needed when using a connection to a function and 
# we need to transmit a variable
#===============================================================================
if sys.version_info[:2] < (2, 5):
    def partial(func, arg):
        def callme():
            return func(arg)
        return callme
else:
    from functools import partial

# < the end >--------------------------------------------------------------------------------------
