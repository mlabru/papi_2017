#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
wid_plot_papi

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

# control
import control.pc_defs as gdefs

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# ângulo de transição baixo (caixa 1)
M_ANG_A = 2.50

# ângulo de transição médio-baixo (caixa 2)
M_ANG_B = 2.83

# ângulo de transição médio-alto (caixa 3)
M_ANG_D = 3.17

# ângulo de transição alto (caixa 4)
M_ANG_E = 3.50

# ângulo normal da rampa
M_ANG_C = (M_ANG_B + M_ANG_D) / 2.

# ângulo de altura mínima do olho do piloto
M_ANG_M = M_ANG_B - 0.033

# superfície de proteção de obtáculo
M_ANG_OPS = M_ANG_A - 0.57

# < CWidgetPlotPAPI >------------------------------------------------------------------------------

class CWidgetPlotPAPI(QtGui.QWidget):
    """
    plot PAPI graphics
    """
    # signal
    C_SGN_NEW_DATA = QtCore.pyqtSignal(float)
    C_SGN_PAGE_ON = QtCore.pyqtSignal(bool)

    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_parent=None):
        """
        constructor

        @param f_parent: parent widget
        """
        # check input
        # assert f_camera_feed

        # init super class
        super(CWidgetPlotPAPI, self).__init__(f_parent)

        # distância em metros
        self.__parent = f_parent
        
        # distância em metros
        self.__f_dst = 60.
        
        # altura atual em metros
        self.__f_alt = 0.

        # altura máxima em metros
        self.__f_alt_max = self.__f_dst * math.sin(math.radians(M_ANG_E + 0.5))

        # setup user interface
        self.__setup_ui(self)

        # create toolBar
        self.__create_toolbar(f_parent)

        # setup PAPI lines
        self.__setup_lines()

        # connect new data signal
        self.C_SGN_NEW_DATA.connect(self.__on_new_data)
        self.C_SGN_PAGE_ON.connect(self.__on_page_on)

    # ---------------------------------------------------------------------------------------------
    def __create_toolbar(self, f_parent):
        """
        create toolbar
        """
        # create toolBar base
        self.__tbr_plot = f_parent.addToolBar(self.tr("plotPAPI"))
        assert self.__tbr_plot is not None

        # start
        self.__tbr_plot.addAction(f_parent.create_action(self.tr("S&tart"), f_shortcut="Ctrl+T",
            f_icon="start.png", f_slot=self.on_act_start, f_tip=self.tr("Start calibration")))

        # stop
        self.__tbr_plot.addAction(f_parent.create_action(self.tr("St&op"), f_shortcut="Ctrl+O",
            f_icon="stop.png", f_slot=self.on_act_stop, f_tip=self.tr("Stop calibration")))

        # separator
        self.__tbr_plot.addSeparator()

        # clear
        self.__tbr_plot.addAction(f_parent.create_action(self.tr("&Clear"), f_shortcut="Ctrl+C",
            f_icon="clear.png", f_slot=self.on_act_clear, f_tip=self.tr("Clear plot")))

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def on_act_clear(self):
        """
        button clear clicked
        """
        # desenha o canvas
        self.__drawing.clear()

        # desenha o canvas
        self.__canvas.draw()

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def on_act_start(self):
        """ 
        start PAPI Calibra : com_monitor thread and the update timer
        """
        # get port comboBox current index
        #li_ndx = self.cbx_port.currentIndex()
        # get current selected port
        #ls_port = self.__lst_available_tty[li_ndx]

        # get baud comboBox current index
        #li_ndx = self.cbx_baud.currentIndex()
        # get current selected baud
        #li_baud = self.__lst_available_baud[li_ndx]

        # disable start button
        #self.btn_start.setEnabled(False)
        # enable stop button 
        #self.btn_stop.setEnabled(True)
        # disable port comboBox
        #self.cbx_port.setEnabled(False)
        # disable baud comboBox
        #self.cbx_baud.setEnabled(False)

        # create TTYMonitorStart event
        #l_evt = evttty.CTTYMonitorStart(ls_port, li_baud)
        #assert l_evt

        # send event
        #self.__event.post(l_evt)

        # config timer update method
        #self.__timer_update.timeout.connect(self.__on_timer)

        # get update frequency
        #lf_update_freq = self.__knb_update_freq.value()

        #if lf_update_freq > 0:
            # start timer update
            #self.__timer_update.start(1000. / lf_update_freq)

        # update statusBar
        #self.__lbl_status.setText("Monitor running")

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def on_act_stop(self):
        """ 
        stop PAPI Calibra
        """
        #if self.com_monitor is not None:
            #self.com_monitor.join(1000)
            #self.com_monitor = None

        # reset flag
        #self.monitor_active = False

        # enable start button
        #self.btn_start.setEnabled(True)
        # disable stop button
        #self.btn_stop.setEnabled(False)
        # enable tty port comboBox
        #self.cbx_port.setEnabled(True)

        # stops update timer
        #self.__timer_update.stop()

        # update status bar
        #self.__lbl_status.setText("Monitor idle")

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(float)
    def on_dsb_dst_valueChanged(self, ff_val):
        """
        spinBox distância valueChanged
        """
        # save new distance
        self.__f_dst = ff_val

        # axes rescale
        self.__drawing.set_xlim(0, ff_val)
        self.__drawing.set_ylim(0, ff_val * math.sin(math.radians(M_ANG_E + 0.5)))

        self.__on_new_data(ff_val / 15.)

        # redraw canvas
        self.__canvas.draw()

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(float)
    def __on_new_data(self, ff_alt):
        """
        received new elevation callback
        """
        # salva nova altura
        self.__f_alt = ff_alt

        l_x = [0., self.__f_dst]  
        l_y = [0., self.__f_alt] 

        llbl_gr = u"{:4.3f}°".format(math.degrees(math.atan2(self.__f_alt, self.__f_dst)))

        self.__line_A.set_data(l_x, l_y)
        self.__line_A.set_label(llbl_gr)
        
        # desenha o canvas
        self.__canvas.draw()

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(bool)
    def __on_page_on(self, fv_on):
        """
        page PAPI activated
        """
        self.__tbr_plot.setEnabled(fv_on)
        self.__tbr_plot.setVisible(fv_on)
        
    # ---------------------------------------------------------------------------------------------
    def __setup_lines(self):
        """
        create PAPI lines
        """
        # initial data
        l_x = [0., self.__f_dst]  
        l_y = [0., self.__f_alt] 

        # label
        llbl_gr = u"{:4.3f}°".format(math.degrees(math.atan2(self.__f_alt, self.__f_dst)))

        l_y = [0., 2.] 

        # limite inferior ângulo de transição baixo (caixa 1)
        self.__line_A_I = CPlotLine(l_x, l_y, mfc='red', ms=12, label=llbl_gr)
        assert self.__line_A_I
        
        # setup
        self.__line_A_I.text.set_color('red')
        self.__line_A_I.text.set_fontsize(8)

        # draw line
        self.__drawing.add_line(self.__line_A_I)
        

        l_y = [0., 4.] 

        # ângulo de transição baixo (caixa 1)
        self.__line_A = CPlotLine(l_x, l_y, mfc='red', ms=12, label=llbl_gr)
        assert self.__line_A
        
        # setup
        self.__line_A.text.set_color('red')
        self.__line_A.text.set_fontsize(8)

        # draw line
        self.__drawing.add_line(self.__line_A)
        

        l_y = [0., 6.] 

        # limite superior ângulo de transição baixo (caixa 1)
        self.__line_A_S = CPlotLine(l_x, l_y, mfc='red', ms=12, label=llbl_gr)
        assert self.__line_A_S
        
        # setup
        self.__line_A_S.text.set_color('red')
        self.__line_A_S.text.set_fontsize(8)

        # draw line
        self.__drawing.add_line(self.__line_A_S)

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

        # create font
        l_font = QtGui.QFont()
        assert l_font

        # setup
        l_font.setBold(True)
        l_font.setWeight(75)

        # groupBox distância
        lgbx_dst = QtGui.QGroupBox(u"Distância")
        assert lgbx_dst
        
        # spinBox distância
        self.__dsb_dst = QtGui.QDoubleSpinBox()
        assert self.__dsb_dst

        # setup
        self.__dsb_dst.setMaximum(500.)
        self.__dsb_dst.setMinimum(60.)
        self.__dsb_dst.setValue(self.__f_dst)
        
        # connect spinBox
        self.__dsb_dst.valueChanged.connect(self.on_dsb_dst_valueChanged)

        # create gbx layout
        llay_dst = QtGui.QVBoxLayout(lgbx_dst)
        assert llay_dst is not None

        # setup
        llay_dst.addWidget(self.__dsb_dst)

        # groupBox pto zero 
        lgbx_zero = QtGui.QGroupBox(u"Pto.Zero")
        assert lgbx_zero

        # labels lat/lng/alt
        self.__lbl_lat = QtGui.QLabel("Lat:\t{}".format(-23.2463))
        assert self.__lbl_lat

        self.__lbl_lng = QtGui.QLabel("Lng:\t{}".format(-45.8542))
        assert self.__lbl_lng

        self.__lbl_alt = QtGui.QLabel("Alt:\t{}".format(self.__f_alt))
        assert self.__lbl_alt

        # create gbx layout
        llay_ptz = QtGui.QVBoxLayout(lgbx_zero)
        assert llay_ptz is not None

        # setup
        llay_ptz.addWidget(self.__lbl_lat)
        llay_ptz.addWidget(self.__lbl_lng)
        llay_ptz.addWidget(self.__lbl_alt)

        # widget buttons
        lwid_btn = QtGui.QWidget()
        assert lwid_btn

        # start button
        lbtn_start = QtGui.QPushButton("start")
        assert lbtn_start

        # setup
        lbtn_start.setIcon(QtGui.QIcon(QtGui.QPixmap(":/images/start.png")))

        # clear screen button
        lbtn_clear = QtGui.QPushButton("clear plot")
        assert lbtn_clear

        # setup
        lbtn_clear.setIcon(QtGui.QIcon(QtGui.QPixmap(":/images/clear.png")))

        # connect clear plot button        
        lbtn_clear.clicked.connect(self.on_act_clear)

        # create buttons layout
        llay_btn = QtGui.QVBoxLayout(lwid_btn)
        assert llay_btn is not None

        # setup
        llay_btn.addWidget(lbtn_start)
        llay_btn.addWidget(lbtn_clear)

        # frame
        l_frm = QtGui.QFrame()
        assert l_frm
        
        # setup
        l_frm.setMaximumHeight(150)
        l_frm.setFrameShape(QtGui.QFrame.StyledPanel)
        l_frm.setFrameShadow(QtGui.QFrame.Raised)

        # frame layout
        llay_frm = QtGui.QHBoxLayout(l_frm)
        assert llay_frm is not None

        # setup
        llay_frm.addWidget(lgbx_dst)
        llay_frm.addWidget(lgbx_zero)
        llay_frm.addWidget(lwid_btn)

        # create plot layout
        llay_plt = QtGui.QVBoxLayout(f_parent)
        assert llay_plt is not None

        # setup
        llay_plt.addWidget(self.__canvas)
        llay_plt.addWidget(l_frm)

# < CPlotLine >------------------------------------------------------------------------------------

class CPlotLine(lines.Line2D):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        # we'll update the position when the line data is set
        self.text = mtext.Text(0, 0, '')
        lines.Line2D.__init__(self, *args, **kwargs)

        # we can't access the label attr until *after* the line is
        # inited
        self.text.set_text(self.get_label())

    # ---------------------------------------------------------------------------------------------
    def draw(self, renderer):
        # draw my label at the end of the line with 2 pixel offset
        lines.Line2D.draw(self, renderer)
        self.text.draw(renderer)

    # ---------------------------------------------------------------------------------------------
    def set_axes(self, axes):
        self.text.set_axes(axes)
        lines.Line2D.set_axes(self, axes)

    # ---------------------------------------------------------------------------------------------
    def set_data(self, x, y):
        if len(x):
            self.text.set_position((x[-1], y[-1]))

        lines.Line2D.set_data(self, x, y)

    # ---------------------------------------------------------------------------------------------
    def set_figure(self, figure):
        self.text.set_figure(figure)
        lines.Line2D.set_figure(self, figure)

    # ---------------------------------------------------------------------------------------------
    def set_transform(self, transform):
        # 2 pixel offset
        texttrans = transform + mtransforms.Affine2D().translate(2, 2)
        self.text.set_transform(texttrans)
        lines.Line2D.set_transform(self, transform)

# < the end >--------------------------------------------------------------------------------------
