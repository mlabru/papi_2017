#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
wid_papi_light_box

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

# PyQt4
from PyQt4 import QtGui
from PyQt4 import QtCore

# view
import wid_light_box as wlbx

# control
import control.pc_defs as gdefs

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CPAPILightBoxWidget >--------------------------------------------------------------------------------

class CPAPILightBoxWidget(QtGui.QGroupBox):
    """
    PAPI lights box
    """
    # signal
    C_SGN_DATA_ALT = QtCore.pyqtSignal(list)

    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_title, f_parent=None):
        """
        constructor
        """
        # init super class
        super(CPAPILightBoxWidget, self).__init__(f_title, f_parent)

        # altitude atual
        self.__f_alt = 0.

        # setupUI
        self.__setup_ui()

        # make connections
        self.C_SGN_DATA_ALT.connect(self.on_data_alt)

        # create state machine
        self.create_state_machine()

    # ---------------------------------------------------------------------------------------------
    def create_light_state(self, lights, duration, parent=None):
        """
        create light state
        """
        lightState = QtCore.QState(parent)
        assert lightState

        # create timer
        timer = QtCore.QTimer(lightState)
        timer.setInterval(duration)
        timer.setSingleShot(True)

        # create internal state
        timing = QtCore.QState(lightState)
        timing.entered.connect(timer.start)

        for light in lights:
            timing.entered.connect(light.turnOn)
            timing.exited.connect(light.turnOff)

        done = QtCore.QFinalState(lightState)

        timing.addTransition(timer, QtCore.SIGNAL("timeout()"), done)

        lightState.setInitialState(timing)

        # return
        return lightState

    # ---------------------------------------------------------------------------------------------
    def create_state_machine(self):
        """
        create state machine
        """
        # subindo
        red2Pink = self.create_light_state([self.__light_box.red_light, self.__light_box.white_light], 1000)
        pink2White = self.create_light_state([self.__light_box.white_light], 1000)

        # descendo
        white2Pink = self.create_light_state([self.__light_box.red_light, self.__light_box.white_light], 1000)
        pink2Red = self.create_light_state([self.__light_box.red_light], 1000)

        # transitions
        red2Pink.addTransition(red2Pink, QtCore.SIGNAL("finished()"), pink2White)
        pink2White.addTransition(pink2White, QtCore.SIGNAL("finished()"), white2Pink)
        white2Pink.addTransition(white2Pink, QtCore.SIGNAL("finished()"), pink2Red)
        pink2Red.addTransition(pink2Red, QtCore.SIGNAL("finished()"), red2Pink)

        # state machine 
        l_machine = QtCore.QStateMachine(self)
        assert l_machine

        # setup
        l_machine.addState(red2Pink)
        l_machine.addState(pink2White)
        l_machine.addState(white2Pink)
        l_machine.addState(pink2Red)

        l_machine.setInitialState(red2Pink)
        l_machine.start()

    # ---------------------------------------------------------------------------------------------
    def on_btn_r2p(self):
        """
        transição de vermelho -> rosa
        """
        # calcula os graus
                
        # traça o gráfico

    # ---------------------------------------------------------------------------------------------
    def on_btn_p2w(self):
        """
        transição de rosa -> branco
        """
    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(list)
    def on_data_alt(self, flst_data):
        """
        new altimeter data arrived
        """
        # save sample time stamp
        self.__l_time = int(flst_data[0])

        # save altimeter data
        self.__f_alt = float(flst_data[3])

    # ---------------------------------------------------------------------------------------------
    def __setup_ui(self):
        """
        setup ui
        """
        # create light box
        self.__light_box = wlbx.CLightBoxWidget()
        assert self.__light_box

        # setup
        self.__light_box.resize(55, 100)
        self.__light_box.show()

        # create label altura V2P
        llbl_alt_r2p = QtGui.QLabel("Alt:")
        assert llbl_alt_r2p

        # create label graus V2P
        llbl_dgr_r2p = QtGui.QLabel("Gr.:")
        assert llbl_dgr_r2p

        # create button V2P
        lbtn_r2p = QtGui.QPushButton("V->R")
        assert lbtn_r2p

        # make connections
        lbtn_r2p.clicked.connect(self.on_btn_r2p)

        # create label altura P2W
        llbl_alt_p2w = QtGui.QLabel("Alt:")
        assert llbl_alt_p2w

        # create label graus V2P
        llbl_dgr_p2w = QtGui.QLabel("Gr.:")
        assert llbl_dgr_p2w

        # create button V2P
        lbtn_p2w = QtGui.QPushButton("R->B")
        assert lbtn_p2w

        # make connections
        lbtn_r2p.clicked.connect(self.on_btn_p2w)

        # create layout
        llo_gbx = QtGui.QGridLayout()
        assert llo_gbx is not None

        llo_gbx.addWidget(self.__light_box, 0, 0, -1, 1)

        llo_gbx.addWidget(llbl_alt_r2p, 0, 1, 1, 2)
        llo_gbx.addWidget(llbl_dgr_r2p, 1, 1, 1, 2)
 
        llo_gbx.addWidget(llbl_alt_p2w, 3, 1, 1, 2)
        llo_gbx.addWidget(llbl_dgr_p2w, 4, 1, 1, 2)
 
        llo_gbx.addWidget(lbtn_r2p, 0, 3, 2, 1)
        llo_gbx.addWidget(lbtn_p2w, 3, 3, 2, 1)

        llo_gbx.setContentsMargins(4, 4, 4, 4)

        # groubBox layout         
        self.setLayout(llo_gbx)

        # groubBox style sheet
        self.setStyleSheet(gdefs.D_GBX_STYLE)

        # setup
        self.setMaximumHeight(143)
        self.setMaximumWidth(275)

# < the end >--------------------------------------------------------------------------------------
