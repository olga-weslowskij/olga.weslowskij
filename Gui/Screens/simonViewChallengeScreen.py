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
from Gui.Screens.simonGameScreen import SimonGameScreen
from Gui.Widgets.viewStream2Widget import ViewStream2Widget
import myglobals

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)

class SimonViewChallengeScreen(SimonGameScreen):
    def __init__(self):

        super(SimonViewChallengeScreen,self).__init__()
        self.mystate = self.__class__.__name__
        self.pianoSimonGame=None

        self.notesscroller = ViewStream2Widget()
        #self.challenge = myglobals.SimonMode.activeChallenge().challenge
        self.challenge = None


    #def on_enter(self, tostate):
    #    SimonGameScreen.on_enter(self,tostate)


    def update(self):
        # poor mans init
        if self.challenge is None and myglobals.SimonMode.activeChallenge():
            self.challenge = myglobals.SimonMode.activeChallenge().challenge
            self.dirty = True


        if self.challenge:
            #self.notesscroller.stream = myglobals.SimonMode.activeChallenge().challenge.innotes

            # get a streams we take the first one, (we have only one at the moment)
            #self.notesscroller.toshow = self.challenge.jumpToStates.knownStreams[0]
            #self.notesscroller.toshow = myglobals.SimonMode.activeChallenge().olgapartStream
            ##self.notesscroller.toshow = myglobals.SimonMode.activeChallenge().allpart
            #self.notesscroller.toshow = myglobals.SimonMode.activeChallenge().challenge.song.mystream
            #self.dirty = True
            #SimonRequests.createShowBestActiveStream(None)
            pass

    def updateGui(self):
        #self.notesscroller.updateGui()
        self.notesscroller.updateGui()
        pass

