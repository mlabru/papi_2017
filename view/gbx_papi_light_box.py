#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
gbx_papi_light_box

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

# PyQt4
from PyQt4 import QtGui
from PyQt4 import QtCore

# view
import wid_light_box as wlbx

# control
import control.pc_defs as gdefs
import control.events.events_basic as events

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CPAPILightBoxWidget >--------------------------------------------------------------------------

class CPAPILightBoxWidget(QtGui.QGroupBox):
    """
    PAPI lights box
    """
    # signal
    C_SGN_DATA_ALT = QtCore.pyqtSignal(list)
    C_SGN_NEW_DIST = QtCore.pyqtSignal(float)
    C_SGN_RESET = QtCore.pyqtSignal()

    C_SGN_PLOT_R2P = QtCore.pyqtSignal(int, float)
    C_SGN_PLOT_P2W = QtCore.pyqtSignal(int, float)

    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_title, fi_box, f_parent):
        """
        constructor

        @param f_title: groupBox title
        @param fi_box: box no.
        @param f_parent: parent widget
        """
        # check input
        assert f_parent
        
        # init super class
        super(CPAPILightBoxWidget, self).__init__(f_title, f_parent)

        # events
        self.__event = f_parent.evtmgr
        assert self.__event

        # register as event listener
        self.__event.register_listener(self)

        # save box no.
        self.__i_box = fi_box

        # altitude atual
        self.__f_alt = 0.

        # distância atual
        self.__f_dist = gdefs.D_DFL_DIST

        # timestamp
        self.__f_time = 0

        # setup UI
        self.__setup_ui()

        # create states
        self.__lst_states = self.create_states(self.__wid_light_box)
        assert self.__lst_states

        # create state machine
        self.__state_machine = self.create_state_machine(self.__lst_states)
        assert self.__state_machine

        # start state machine
        self.__state_machine.start()

        # make connections
        self.C_SGN_DATA_ALT.connect(self.__on_data_alt)
        self.C_SGN_NEW_DIST.connect(self.__on_new_dist)

    # ---------------------------------------------------------------------------------------------
    def create_light_state(self, f_lights, f_parent=None):
        """
        create light state
        """
        # create light state
        l_lightState = QtCore.QState(f_parent)
        assert l_lightState

        # for all lights...
        for l_light in f_lights:
            # make connections
            l_lightState.entered.connect(l_light.turnOn)
            l_lightState.exited.connect(l_light.turnOff)

        # return
        return l_lightState

    # ---------------------------------------------------------------------------------------------
    def create_state_machine(self, flst_states):
        """
        create state machine

        @param flst_states: states (initial state is the first one) 
        """
        # check input
        assert flst_states 

        # state machine 
        l_machine = QtCore.QStateMachine(self)
        assert l_machine

        # for all states...
        for l_stt in flst_states:
            # add state to machine
            l_machine.addState(l_stt)

        # set initial state
        l_machine.setInitialState(flst_states[0])

        # return
        return l_machine

    # ---------------------------------------------------------------------------------------------
    def create_states(self, f_light_box):
        """
        create state machine
        """
        # check input
        assert f_light_box 

        # states
        lstt_red = self.create_light_state([f_light_box.red_light])
        lstt_pink = self.create_light_state([f_light_box.red_light, f_light_box.white_light])
        lstt_white = self.create_light_state([f_light_box.white_light])

        # transitions
        lstt_red.addTransition(self.__btn_r2p, QtCore.SIGNAL("clicked()"), lstt_pink)
        lstt_pink.addTransition(self.__btn_p2w, QtCore.SIGNAL("clicked()"), lstt_white)

        lstt_pink.addTransition(self.C_SGN_RESET, lstt_red)
        lstt_white.addTransition(self.C_SGN_RESET, lstt_red)

        # return
        return [lstt_red, lstt_pink, lstt_white] 

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
            # reset light box
            self.__on_evt_reset()

    # ---------------------------------------------------------------------------------------------
    def __on_btn_r2p(self):
        """
        transição de vermelho -> rosa
        """
        # altitude setup
        self.__lbl_alt_r2p.setText(u"Alt.:\t{:4.3f}m".format(self.__f_alt))
        self.__lbl_alt_r2p.setStyleSheet("QLabel { background-color: lightgray; color: green; }")

        # degrees setup
        self.__lbl_dgr_r2p.setText(u"Deg.:\t{:4.3f}°".format(math.degrees(math.atan2(self.__f_alt, self.__f_dist))))
        self.__lbl_dgr_r2p.setStyleSheet("QLabel { background-color: lightgray; color: green; }")
                
        # emit plot signal
        self.C_SGN_PLOT_R2P.emit(self.__i_box, self.__f_alt)

    # ---------------------------------------------------------------------------------------------
    def __on_btn_p2w(self):
        """
        transição de rosa -> branco
        """
        # altitude setup
        self.__lbl_alt_p2w.setText(u"Alt.:\t{:4.3f}m".format(self.__f_alt))
        self.__lbl_alt_p2w.setStyleSheet("QLabel { background-color: lightgray; color: green; }")

        # degrees setup
        self.__lbl_dgr_p2w.setText(u"Deg.:\t{:4.3f}°".format(math.degrees(math.atan2(self.__f_alt, self.__f_dist))))
        self.__lbl_dgr_p2w.setStyleSheet("QLabel { background-color: lightgray; color: green; }")
                
        # emit plot signal
        self.C_SGN_PLOT_P2W.emit(self.__i_box, self.__f_alt)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(list)
    def __on_data_alt(self, flst_data):
        """
        new altimeter data arrived
        """
        # save sample time stamp
        self.__f_time = float(flst_data[0])

        # save altimeter data
        self.__f_alt = float(flst_data[3])

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_evt_reset(self):
        """
        event CReset
        """
        # reset state machine
        self.C_SGN_RESET.emit()
        
        # reset texts
        self.__lbl_alt_r2p.setText("")
        self.__lbl_dgr_r2p.setText("")

        self.__lbl_alt_p2w.setText("")
        self.__lbl_dgr_p2w.setText("")

        # save distance
        self.__f_dist = gdefs.D_DFL_DIST

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(float)
    def __on_new_dist(self, ff_dist):
        """
        new distance data arrived
        """
        # save distance
        self.__f_dist = ff_dist

    # ---------------------------------------------------------------------------------------------
    def __setup_ui(self):
        """
        setup ui
        """
        # create light box
        self.__wid_light_box = wlbx.CLightBoxWidget()
        assert self.__wid_light_box

        # setup
        self.__wid_light_box.resize(55, 100)
        self.__wid_light_box.show()

        # create label altura V2P
        self.__lbl_alt_r2p = QtGui.QLabel()
        assert self.__lbl_alt_r2p

        # create label graus V2P
        self.__lbl_dgr_r2p = QtGui.QLabel()
        assert self.__lbl_dgr_r2p

        # create button V2P
        self.__btn_r2p = QtGui.QPushButton("V->R")
        assert self.__btn_r2p

        # setup
        self.__btn_r2p.setMinimumHeight(44)

        # make connections
        self.__btn_r2p.clicked.connect(self.__on_btn_r2p)

        # create label altura P2W
        self.__lbl_alt_p2w = QtGui.QLabel()
        assert self.__lbl_alt_p2w

        # create label graus V2P
        self.__lbl_dgr_p2w = QtGui.QLabel()
        assert self.__lbl_dgr_p2w

        # create button V2P
        self.__btn_p2w = QtGui.QPushButton("R->B")
        assert self.__btn_p2w

        # setup
        self.__btn_p2w.setMinimumHeight(44)

        # make connections
        self.__btn_p2w.clicked.connect(self.__on_btn_p2w)

        # create layout
        llo_gbx = QtGui.QGridLayout()
        assert llo_gbx is not None

        llo_gbx.addWidget(self.__wid_light_box, 0, 0, -1, 1)

        llo_gbx.addWidget(self.__lbl_alt_p2w, 0, 1, 1, 2)
        llo_gbx.addWidget(self.__lbl_dgr_p2w, 1, 1, 1, 2)
 
        llo_gbx.addWidget(self.__lbl_alt_r2p, 3, 1, 1, 2)
        llo_gbx.addWidget(self.__lbl_dgr_r2p, 4, 1, 1, 2)
 
        llo_gbx.addWidget(self.__btn_p2w, 0, 3, 2, 1)
        llo_gbx.addWidget(self.__btn_r2p, 3, 3, 2, 1)

        llo_gbx.setContentsMargins(4, 4, 4, 4)

        # groubBox layout         
        self.setLayout(llo_gbx)

        # groubBox style sheet
        self.setStyleSheet(gdefs.D_GBX_STYLE)

        # setup
        self.setMaximumHeight(143)
        self.setMaximumWidth(275)

# < the end >--------------------------------------------------------------------------------------
