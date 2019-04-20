#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
gbx_config

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

# control
import control.pc_defs as gdefs
import control.events.events_basic as events

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CConfigWidget >--------------------------------------------------------------------------------

class CConfigWidget(QtGui.QGroupBox):
    """
    plot PAPI graphics
    """
    # signal
    C_SGN_NEW_DIST = QtCore.pyqtSignal(float)
    C_SGN_PAGE_ON = QtCore.pyqtSignal(bool)

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
        super(CConfigWidget, self).__init__(fs_title, f_parent)

        # events
        self.__event = f_parent.evtmgr
        assert self.__event

        # distância em metros
        self.__f_dst = gdefs.D_DFL_DIST
        
        # altura atual em metros
        self.__f_alt = 0.

        # setup user interface
        self.__setup_ui()

        # create toolBar
        self.__create_toolbar(f_parent)

        # connect new data signal
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
        lact_start = f_parent.create_action(self.tr("S&tart"), f_shortcut="Ctrl+T",
            f_icon="start.png", f_slot=self.on_act_start, f_tip=self.tr("Start calibration"))

        lact_start.setEnabled(False)

        self.__tbr_plot.addAction(lact_start)

        # stop
        lact_stop = f_parent.create_action(self.tr("St&op"), f_shortcut="Ctrl+O",
            f_icon="stop.png", f_slot=self.on_act_stop, f_tip=self.tr("Stop calibration"))

        lact_stop.setEnabled(False)

        self.__tbr_plot.addAction(lact_stop)

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
    @QtCore.pyqtSlot(bool)
    def __on_btn_reset_clicked(self, fv_val):
        """
        pushButton reset clicked
        """
        # distância em metros
        self.__f_dst = gdefs.D_DFL_DIST
        
        # altura atual em metros
        self.__f_alt = 0.

        # reset spinBox
        self.__dsb_dst.setValue(self.__f_dst)

        # emit signal
        self.C_SGN_NEW_DIST.emit(self.__f_dst)

        # create CReset event
        l_evt = events.CReset()
        assert l_evt

        # dispatch event
        self.__event.post(l_evt)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(float)
    def __on_dsb_dst_valueChanged(self, ff_val):
        """
        spinBox distância valueChanged
        """
        # save new distance
        self.__f_dst = ff_val

        # emit signal
        self.C_SGN_NEW_DIST.emit(ff_val)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(bool)
    def __on_page_on(self, fv_on):
        """
        page PAPI activated
        """
        self.__tbr_plot.setEnabled(fv_on)
        self.__tbr_plot.setVisible(fv_on)
        
    # ---------------------------------------------------------------------------------------------
    def __setup_ui(self):
        """
        setup user interface
        """
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
        self.__dsb_dst.setMaximum(gdefs.D_MAX_DIST)
        self.__dsb_dst.setMinimum(gdefs.D_DFL_DIST)
        self.__dsb_dst.setValue(self.__f_dst)
        
        # connect spinBox
        self.__dsb_dst.valueChanged.connect(self.__on_dsb_dst_valueChanged)

        # create gbx layout
        llay_dst = QtGui.QVBoxLayout(lgbx_dst)
        assert llay_dst is not None

        # setup
        llay_dst.addWidget(self.__dsb_dst)

        # groupBox pto zero 
        lgbx_zero = QtGui.QGroupBox(u"Pto.Zero")
        assert lgbx_zero

        # labels lat/lng/alt
        llbl_lat = QtGui.QLabel("Lat.:")
        assert llbl_lat

        llbl_lng = QtGui.QLabel("Lng.:")
        assert llbl_lng

        llbl_alt = QtGui.QLabel("Alt.:")
        assert llbl_alt

        # QLineEdit lat/lng/alt
        self.__qle_lat = QtGui.QLineEdit()
        assert self.__qle_lat

        self.__qle_lng = QtGui.QLineEdit()
        assert self.__qle_lng

        self.__qle_alt = QtGui.QLineEdit()
        assert self.__qle_alt

        # labels lat/lng/alt
        self.__lbl_lat = QtGui.QLabel("{:5.3}".format(-23.2463))
        assert self.__lbl_lat

        self.__lbl_lng = QtGui.QLabel("{:5.3}".format(-45.8542))
        assert self.__lbl_lng

        self.__lbl_alt = QtGui.QLabel("{:5.3}".format(self.__f_alt))
        assert self.__lbl_alt

        # create gbx layout
        llay_ptz = QtGui.QGridLayout(lgbx_zero)
        assert llay_ptz is not None

        # setup
        llay_ptz.addWidget(llbl_lat, 0, 0)
        llay_ptz.addWidget(llbl_lng, 1, 0)
        llay_ptz.addWidget(llbl_alt, 2, 0)

        llay_ptz.addWidget(self.__qle_lat, 0, 1)
        llay_ptz.addWidget(self.__qle_lng, 1, 1)
        llay_ptz.addWidget(self.__qle_alt, 2, 1)

        llay_ptz.addWidget(self.__lbl_lat, 0, 2)
        llay_ptz.addWidget(self.__lbl_lng, 1, 2)
        llay_ptz.addWidget(self.__lbl_alt, 2, 2)

        # widget buttons
        lwid_btn = QtGui.QWidget()
        assert lwid_btn

        # start button
        lbtn_start = QtGui.QPushButton("&Start")
        assert lbtn_start

        # setup
        lbtn_start.setIcon(QtGui.QIcon(QtGui.QPixmap(":/images/start.png")))
        lbtn_start.setEnabled(False)

        # reset screen button
        lbtn_reset = QtGui.QPushButton("&Reset")
        assert lbtn_reset

        # setup
        lbtn_reset.setIcon(QtGui.QIcon(QtGui.QPixmap(":/images/clear.png")))

        # connect reset plot button        
        lbtn_reset.clicked.connect(self.__on_btn_reset_clicked)

        # create buttons layout
        llay_btn = QtGui.QVBoxLayout(lwid_btn)
        assert llay_btn is not None

        # setup
        llay_btn.addWidget(lbtn_start)
        llay_btn.addWidget(lbtn_reset)

        # frame
        l_frm = QtGui.QFrame()
        assert l_frm
        
        # setup
        l_frm.setFrameShape(QtGui.QFrame.StyledPanel)
        l_frm.setFrameShadow(QtGui.QFrame.Raised)

        # frame layout
        llay_frm = QtGui.QVBoxLayout(l_frm)
        assert llay_frm is not None

        # setup
        llay_frm.addWidget(lgbx_dst)
        llay_frm.addWidget(lgbx_zero)
        llay_frm.addWidget(lwid_btn)

        # create plot layout
        llay_plt = QtGui.QVBoxLayout(self)
        assert llay_plt is not None

        # setup
        llay_plt.addWidget(l_frm)

# < the end >--------------------------------------------------------------------------------------
