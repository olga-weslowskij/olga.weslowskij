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

from Gui.myState import MyState
import myglobals

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ +  '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)



class MyScreen(MyState):
    def __init__(self):
        # default
        self.parentwidget=myglobals.ScreenState.root
        self.widget=None
        self.dirty= True
        self.mystate=self.__class__.__name__

        self.selectedobject =None

    def show(self, abool):
        if abool:
            try:
                self.parentwidget.remove_widget(self.widget)
            except:
                pass

            self.parentwidget.add_widget(self.widget)
        else:
            self.parentwidget.remove_widget(self.widget)

    def on_leave(self, tostate):
        self.show(False)

    def on_enter(self, tostate):
        self.show(True)
        #self.updateGui()

    def updateGui(self):
        self.dirty = False
        pass


