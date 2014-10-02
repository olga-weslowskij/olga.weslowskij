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
from kivy.uix.button import Button
from Gui.Screens.configAChallengeOptionsScreen import ConfigAChallengeOptionsScreen
from myglobals import ScreenState
import myglobals
from Game.options import getOptionValue

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)

class ConfigOlgaOptionsScreen(ConfigAChallengeOptionsScreen):
    def __init__(self):
        super(ConfigOlgaOptionsScreen,self).__init__()
        #self.mystate=self.__class__.__name__
        print self.mystate
        self.options={}

        #self.options["hand"] = "hand"
        #self.options["speedtol"] = "speedtol"
        #self.options["chorderrors"] = "chorderrors"
        #self.options["repeat"] = "repeat"
        self.options["paused"] = "No"

        self.name = "olga"

        try:
            self.loadOptions()
        except:
            pass

    def build(self, astateName=None):

        super(ConfigOlgaOptionsScreen,self).build(astateName)

        def callback2(instance):
            #myglobals.OlgaMode.challenge.speedtol= getOptionValue("speedtol")
            myglobals.OlgaMode.paused= getOptionValue("paused")
            #self.saveOptions()
            ScreenState.change_state_back()

        btn = Button(text='Done')
        btn.bind(on_press=callback2)

        self.widget.add_widget(btn)
