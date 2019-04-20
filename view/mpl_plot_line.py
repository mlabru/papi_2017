#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
mpl_plot_line

papi calibrate

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

revision 0.1  2017/abr  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.1$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/04"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import math
import sys

# PyQt4
from PyQt4 import QtCore
from PyQt4 import QtGui

# matplotlib
import matplotlib.pyplot as plt
import matplotlib.text as mtext
import matplotlib.lines as lines
import matplotlib.transforms as mtransforms

# control
import control.pc_defs as gdefs

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CPlotLine >------------------------------------------------------------------------------------

class CPlotLine(lines.Line2D):
    """
    plot line
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """
        constructor
        """
        # we'll update the position when the line data is set
        self.text = mtext.Text(0, 0, '')

        # init super class
        lines.Line2D.__init__(self, *args, **kwargs)

        # we can't access the label attr until *after* the line is inited
        self.text.set_text(self.get_label())

    # ---------------------------------------------------------------------------------------------
    def draw(self, f_renderer):
        """
        draw
        """
        # draw my label at the end of the line with 2 pixel offset
        lines.Line2D.draw(self, f_renderer)
        self.text.draw(f_renderer)

    # ---------------------------------------------------------------------------------------------
    def set_axes(self, f_axes):
        """
        set axes
        """
        self.text.set_axes(f_axes)
        lines.Line2D.set_axes(self, f_axes)

    # ---------------------------------------------------------------------------------------------
    def set_data(self, f_x, f_y):
        """
        set data
        """
        if len(f_x):
            self.text.set_position((f_x[-1], f_y[-1]))

        lines.Line2D.set_data(self, f_x, f_y)

    # ---------------------------------------------------------------------------------------------
    def set_figure(self, f_figure):
        """
        set figure
        """
        self.text.set_figure(f_figure)
        lines.Line2D.set_figure(self, f_figure)

    # ---------------------------------------------------------------------------------------------
    def set_transform(self, f_transform):
        """
        set transform
        """
        # 2 pixel offset
        l_texttrans = f_transform + mtransforms.Affine2D().translate(2, 2)

        self.text.set_transform(l_texttrans)
        lines.Line2D.set_transform(self, f_transform)

# < the end >--------------------------------------------------------------------------------------
