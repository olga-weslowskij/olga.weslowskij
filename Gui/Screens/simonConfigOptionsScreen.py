# Copyright (C) weslowskij
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import logging
import pdb
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from Gui.Screens.configAChallengeOptionsScreen import ConfigAChallengeOptionsScreen, buildOptionWidget
from myglobals import ScreenState
from Game.options import RecommendOptionsValues, getOptionValue
import myglobals

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)


class SimonConfigOptionsScreen(ConfigAChallengeOptionsScreen):
    def __init__(self):
        super(SimonConfigOptionsScreen,self).__init__()
        #self.mystate=self.__class__.__name__
        #print self.mystate
        self.options={}

        #self.options["hand"] = "hand"
        self.options["speedtol"] = "speedtol"
        #self.options["chorderrors"] = "chorderrors"
        self.options["repeat"] = "repeat"
        self.options["speed"] = "speed"
        self.options["adaptive"] = "adaptive"

        self.optionswidgets={}


    # depricated redirect
    """ messes gui
    def on_enter(self, tostate):
        super(SimonConfigOptionsScreen,self).on_enter(tostate)
        super(SimonConfigOptionsScreen,self).on_leave(tostate)
        myglobals.ScreenState['ConfigObjectScreen'].object = myglobals.gameState.SimonMode
        myglobals.ScreenState['ConfigObjectScreen'].debug = False
        myglobals.ScreenState.change_state('ConfigObjectScreen')
    """


    def build(self, astateName=None):
        # only too build MdidController and fill options midi in and midi out
        #myglobals.gameState = pianoSimonGame.PianoSimonGame()
        #myglobals.gameState = gameEngineRoot.PianoSimonGame2()
        #myglobals.gameState.myMidiController = MyMidiController()

        self.widget = BoxLayout(orientation='vertical')

        #self.fileChooser = FileChooserListView()

        #self.widget.add_widget(self.fileChooser)

        #self.widget.add_widget(buildLabeledTextWidget(text="client"))
        #self.widget.add_widget(buildLabeledTextWidget(text="port"))
        #self.widget.add_widget(buildLabeledTextWidget(text="Song"))
        for x in RecommendOptionsValues.keys():
            if self.options.get(x,None) is not None:
                ow = buildOptionWidget(x , self.optionswidgets)
                self.widget.add_widget(ow)

        #optionswidgets["speedtol"].text='easy'
        #optionswidgets["hand"].text='left and right'

        self.loadOptions()

        #self.widget.add_widget(buildLabeledTextWidget(text="Hand"))

        #self.widget.add_widget(buildLabeledTextWidget(text="Timing"))


        def callback2(instance):
            ScreenState.change_state("SimonSelectStartScreen")

        btn2 = Button(text='Show Start Selection Screen')
        btn2.bind(on_press=callback2)

        self.widget.add_widget(btn2)

        def callback21(instance):
            myglobals.SimonMode.speedtol= getOptionValue("speedtol", self.optionswidgets)
            myglobals.SimonMode.repeat= int(getOptionValue("repeat", self.optionswidgets))
            try:
                myglobals.SimonMode.speed= float(getOptionValue("speed", self.optionswidgets))
            except:
                myglobals.SimonMode.speed=None

            myglobals.SimonMode.adaptive= bool(getOptionValue("adaptive", self.optionswidgets))

            # startchord can be messed up (fixed)
            myglobals.SimonMode.initSimonChallenges(astartNote=myglobals.SimonMode.startchord[0])

            #self.saveOptions()

            ScreenState.change_state_back()


        btn21 = Button(text='Done')
        btn21.bind(on_press=callback21)
        self.widget.add_widget(btn21)

        def callback(instance):
            ScreenState.change_state_back()

        btn = Button(text='Back')
        btn.bind(on_press=callback)

        self.widget.add_widget(btn)




        if astateName:
            self.mystate=astateName

        ScreenState.add_state(self)


        return self.widget

