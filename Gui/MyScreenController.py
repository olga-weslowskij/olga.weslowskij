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
from kivy.uix.boxlayout import BoxLayout
from Gui.Screens.myScreen import logger
from Gui.myState import MyStateController
import myglobals

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


class MyScreenController(MyStateController):
    def __init__(self):
        super(MyScreenController,self).__init__()
        self.root=BoxLayout()
        self.dirtyScreens={}

    def __getitem__(self, item):
        #self.dirtyScreens[item] = True
        # TODO dont assume change on get
        self.mystates[item].dirty= True
        return self.mystates[item]

    def change_state(self,newstatestr):
        super(MyScreenController,self).change_state(newstatestr)
        #self.updateGui()

    def change_state_back(self):
        print "Back to " + str(self.mystate.back.mystate)
        self.mystate.back.dirty= True
        self.change_state(self.mystate.back.mystate)


    def add_state(self, astate):
        super(MyScreenController,self).add_state(astate)
        self.dirtyScreens[astate] = True

    def updateGui(self):
        self.mystate.dirty= True

    def update(self):
        self.mystate.update()

        #if self.mystate.dirty and options.getOptionValue("update Gui"):
        if self.mystate.dirty:
            logger.info(str(self.mystate) + " dirty => update")
            self.mystate.updateGui()
            logger.info(str(self.mystate) + " dirty => update done")
            self.mystate.dirty =  False

ScreenState = MyScreenController()
myglobals.ScreenState=ScreenState