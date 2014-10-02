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
from Gui.Screens.aViewNotesScreen import AViewNotesScreen
import myglobals


class LogScreen(AViewNotesScreen):
    def __init__(self):
        super(LogScreen,self).__init__()
        self.mystate = "Log"
        self.pianoSimonGame=None

        self.donelen = 0

    def on_enter(self, tostate):
        super(LogScreen, self).on_enter(tostate)
        #SimonRequests.createShowErrorStream(myglobals.SimonMode.activeChallenge().challenge)

        print self.mystate


    def update(self):
        print "update LogScreen"
        if myglobals.HistoryMode:
            if len(myglobals.HistoryMode.todaystream) > self.donelen:
                #self.dirty = True
                self.updateGui()




    def updateGui(self):
        self.notesscroller.updateGui()
        pass


    def build(self):
        pass







