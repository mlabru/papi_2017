#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
gbx_plot_papi

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

# numPy
import numpy as np

# matplotlib
import matplotlib.pyplot as plt
import matplotlib.text as mtext
import matplotlib.lines as lines
import matplotlib.transforms as mtransforms
import matplotlib.backends.backend_qt4agg as qt4agg

# view
import mpl_plot_line as mpl

# control
import control.pc_defs as gdefs
import control.events.events_basic as events

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CPlotPAPIWidget >------------------------------------------------------------------------------

class CPlotPAPIWidget(QtGui.QGroupBox):
    """
    plot PAPI graphics
    """
    # signal
    C_SGN_NEW_DIST = QtCore.pyqtSignal(float)
    C_SGN_PAGE_ON = QtCore.pyqtSignal(bool)

    C_SGN_PLOT_R2P = QtCore.pyqtSignal(int, float)
    C_SGN_PLOT_P2W = QtCore.pyqtSignal(int, float)

    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_title, f_parent):
        """
        constructor

        @param fs_title: groupBox title
        @param f_parent: parent widget
        """
        # check input
        assert f_parent

        # init super class
        super(CPlotPAPIWidget, self).__init__(fs_title, f_parent)

        # distância em metros
        self.__parent = f_parent
        
        # events
        self.__event = f_parent.evtmgr
        assert self.__event

        # register as event listener
        self.__event.register_listener(self)

        # distância em metros
        self.__f_dst = gdefs.D_DFL_DIST
        
        # altura atual em metros
        self.__f_alt = 0.

        # altura máxima em metros
        self.__f_alt_max = self.__f_dst * math.sin(math.radians(gdefs.D_ANG_MAX))

        # setup user interface
        self.__setup_ui(self)

        # create toolBar
        self.__create_toolbar(f_parent)

        # PAPI line angles (A, B, D, E)
        self.__f_ang = [None for _ in xrange(4)]

        # setup PAPI lines (A, B, D, E)
        self.__line_m = [None for _ in xrange(4)]
        self.__line_i = [None for _ in xrange(4)]

        # connect new data signal
        self.C_SGN_NEW_DIST.connect(self.__on_new_dist)
        self.C_SGN_PAGE_ON.connect(self.__on_page_on)

        self.C_SGN_PLOT_R2P.connect(self.__on_plot_r2p)
        self.C_SGN_PLOT_P2W.connect(self.__on_plot_p2w)

    # ---------------------------------------------------------------------------------------------
    def __create_toolbar(self, f_parent):
        """
        create toolbar
        """
        # create toolBar base
        self.__tbr_plot = f_parent.addToolBar(self.tr("plotPAPI"))
        assert self.__tbr_plot is not None

        # clear
        self.__tbr_plot.addAction(f_parent.create_action(self.tr("&Clear"), f_shortcut="Ctrl+C",
            f_icon="clear.png", f_slot=self.__on_act_clear, f_tip=self.tr("Clear plot")))

    # ---------------------------------------------------------------------------------------------
    # @staticmethod
    def notify(self, f_evt):
        """
        event handling callback
            
        @param f_event: received event
        """
        # check input
        assert f_evt

        # received reset event ?
        if isinstance(f_evt, events.CReset):
            # reset distance
            self.__on_new_dist(gdefs.D_DFL_DIST)
            # clear plot
            self.__on_act_clear()

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_act_clear(self):
        """
        button clear clicked
        """
        # desenha o canvas
        self.__drawing.clear()

        # axes rescale
        self.__drawing.set_xlim(0, self.__f_dst)
        self.__drawing.set_ylim(0, self.__f_alt_max)

        # label dos eixos
        self.__drawing.set_ylabel(u"Elevação")
        self.__drawing.set_xlabel(u"Distância")

        # desenha o canvas
        self.__canvas.draw()

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(float)
    def __on_new_dist(self, ff_dist):
        """
        received new distance callback
        """
        # distância em metros
        self.__f_dst = ff_dist
        self.__f_alt_max = ff_dist * math.sin(math.radians(gdefs.D_ANG_MAX))

        # axes rescale
        self.__drawing.set_xlim(0, self.__f_dst)
        self.__drawing.set_ylim(0, self.__f_alt_max)

        # redraw canvas
        self.__canvas.draw()

        # self.__line_A.set_data(l_x, l_y)
        # self.__line_A.set_label(llbl_gr)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(bool)
    def __on_page_on(self, fv_on):
        """
        page PAPI activated
        """
        self.__tbr_plot.setEnabled(fv_on)
        self.__tbr_plot.setVisible(fv_on)
        
    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(int, float)
    def __on_plot_r2p(self, fi_box, ff_alt):
        """
        plot r2p activated
        """
        # valid box no. ?
        if -1 < fi_box < 4:
            # label
            llbl_gr = u"{:4.3f}°".format(math.degrees(math.atan2(ff_alt, self.__f_dst)))

            l_x = [0., self.__f_dst]  
            l_y = [0., ff_alt] 

            # limite inferior ângulo de transição baixo
            self.__line_i[fi_box] = mpl.CPlotLine(l_x, l_y, c="red", ls="--", lw=1, label=llbl_gr)
            assert self.__line_i[fi_box]
            
            # setup
            self.__line_i[fi_box].text.set_color("red")
            self.__line_i[fi_box].text.set_fontsize(7)

            # draw line
            self.__drawing.add_line(self.__line_i[fi_box])

            # desenha o canvas
            self.__canvas.draw()

        # senão,...
        else:
            # logger
            l_log = logging.getLogger("CPlotPAPIWidget::__on_plot_r2p")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: box {} doesn't exist".format(fi_box))

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(int, float)
    def __on_plot_p2w(self, fi_box, ff_alt):
        """
        plot p2w activated
        """
        # valid box no. ?
        if -1 < fi_box < 4:
            # obtém os dados da linha inferior
            (_, l_y) = self.__line_i[fi_box].get_data()

            l_x = [0., self.__f_dst]  
            l_y = [0., (ff_alt + l_y[1]) / 2.] 

            # hide inferior line
            self.__line_i[fi_box].text.set_text("")
            self.__line_i[fi_box].set_visible(False)

            # determina o ângulo da caixa
            self.__f_ang[fi_box] = math.degrees(math.atan2(l_y[1], self.__f_dst))

            # label da linha
            llbl_gr = u"{} - {:4.3f}°".format(gdefs.D_LINES[fi_box], self.__f_ang[fi_box])

            # limite inferior ângulo de transição baixo
            self.__line_m[fi_box] = mpl.CPlotLine(l_x, l_y, c="green", ls="-", lw=2, label=llbl_gr)
            assert self.__line_m[fi_box]
            
            # setup
            self.__line_m[fi_box].text.set_color("green")
            self.__line_m[fi_box].text.set_fontsize(9)

            # draw line
            self.__drawing.add_line(self.__line_m[fi_box])

            # caixa 1 ?
            if 0 == fi_box:
                # calcula superfície de proteção de obtáculo (ANG_OPS = ANG_A - 0.57)
                lf_ops = self.__f_ang[0] - 0.57
                
                # label da linha
                llbl_gr = u"{} - {:4.3f}°".format("OPS", lf_ops)

                l_x = [0., self.__f_dst]  
                l_y = [0., self.__f_dst * math.sin(math.radians(lf_ops))] 

                # superfície de proteção de obtáculo
                self.__line_ops = mpl.CPlotLine(l_x, l_y, c="blue", ls="-", lw=1, label=llbl_gr)
                assert self.__line_ops
                
                # setup
                self.__line_ops.text.set_color("blue")
                self.__line_ops.text.set_fontsize(7)

                # draw line
                self.__drawing.add_line(self.__line_ops)

            # caixa 2 ?
            elif 1 == fi_box:
                # calcula ângulo de altura mínima do olho do piloto (ANG_M = ANG_B - 0.033)
                lf_pe = self.__f_ang[1] - 0.033
                
                # label da linha
                llbl_gr = u"{} - {:4.3f}°".format("M", lf_pe)

                l_x = [0., self.__f_dst]  
                l_y = [0., self.__f_dst * math.sin(math.radians(lf_pe))] 

                # altura mínima do olho do piloto
                self.__line_pe = mpl.CPlotLine(l_x, l_y, c="blue", ls="-", lw=1, label=llbl_gr)
                assert self.__line_pe
                
                # setup
                self.__line_pe.text.set_color("blue")
                self.__line_pe.text.set_fontsize(7)

                # draw line
                self.__drawing.add_line(self.__line_pe)

            # caixa 4 ?
            elif 3 == fi_box:
                # calcula ângulo normal da rampa (ANG_B + ANG_D) / 2.
                lf_c = (self.__f_ang[1] + self.__f_ang[fi_box]) / 2.
                
                # label da linha
                llbl_gr = u"{} - {:4.3f}°".format("M", lf_c)

                l_x = [0., self.__f_dst]  
                l_y = [0., self.__f_dst * math.sin(math.radians(lf_c))] 

                # altura mínima do olho do piloto
                self.__line_c = mpl.CPlotLine(l_x, l_y, c="black", ls="-", lw=1, label=llbl_gr)
                assert self.__line_c
                
                # setup
                self.__line_c.text.set_color("black")
                self.__line_c.text.set_fontsize(7)

                # draw line
                self.__drawing.add_line(self.__line_c)

            # desenha o canvas
            self.__canvas.draw()

        # senão,...
        else:
            # logger
            l_log = logging.getLogger("CPlotPAPIWidget::__on_plot_p2w")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: box {} doesn't exist".format(fi_box))
            
    # ---------------------------------------------------------------------------------------------
    def __setup_plot(self):
        """
        do plot
        """
        # figure
        l_figure = plt.figure()
        assert l_figure

        # drawing
        self.__drawing = l_figure.add_subplot(111)
        assert self.__drawing

        # escalas dos eixos
        self.__drawing.set_xlim(0, self.__f_dst)
        self.__drawing.set_ylim(0, self.__f_alt_max)

        # label dos eixos
        self.__drawing.set_ylabel(u"Elevação")
        self.__drawing.set_xlabel(u"Distância")

        # canvas
        self.__canvas = qt4agg.FigureCanvasQTAgg(l_figure)
        assert self.__canvas

    # ---------------------------------------------------------------------------------------------
    def __setup_ui(self, f_parent=None):
        """
        setup user interface
        """
        # create plot 
        self.__setup_plot()

        # clear screen button
        lbtn_clear = QtGui.QPushButton("&Clear")
        assert lbtn_clear

        # setup
        lbtn_clear.setIcon(QtGui.QIcon(QtGui.QPixmap(":/images/clear.png")))

        # connect clear plot button        
        lbtn_clear.clicked.connect(self.__on_act_clear)

        # create plot layout
        llay_plt = QtGui.QVBoxLayout(f_parent)
        assert llay_plt is not None

        # setup
        llay_plt.addWidget(self.__canvas)
        llay_plt.addWidget(lbtn_clear)

# < the end >--------------------------------------------------------------------------------------
