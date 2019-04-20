#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
papi calibrate

revision 0.1  2017/abr  mlabru
initial version (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.1$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/04"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import multiprocessing
import sys

# control
import control.pc_control as control

# -------------------------------------------------------------------------------------------------
def main():

    # instancia o controle
    l_control = control.CPAPICalControl()
    assert l_control

    try:
        # obtém a view
        l_view = l_control.view
        assert l_view

        # ativa a viewer
        l_view.run()

    # trata interrupções
    except KeyboardInterrupt as SystemExit:

        # termina a aplicação
        l_control.cbk_termina()

# -------------------------------------------------------------------------------------------------
# this is the bootstrap process

if "__main__" == __name__:

    # logger
    logging.basicConfig()

    # multiprocessing logger
    multiprocessing.log_to_stderr()

    # run application
    main()

    # termina
    sys.exit()

# < the end >--------------------------------------------------------------------------------------
