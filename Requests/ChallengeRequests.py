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
from myglobals import ScreenState
import myglobals

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)


class ChallengeRequests(object):
    def ShowChallenge(self):
        logger.debug("enter ShowChallenge\n")
        #levcha = MyLevenshteinChallenge()
        #levcha = ScreenState["Song"].levcha2
        if self.knownNotesstream is None:
            logger.debug("no stream\n")
            return

        logger.debug("stream done\n")


        #code.interact(local=locals())

        #ret.build(start, end)
        #ret = ret.chordify()
        #print "len(ret) " + str(len(myglobals.OlgaMode.knownNotesstream.song.mystream))

        # "OlgaViewChallengeScreen"
        ScreenState["OlgaViewChallengeScreen"].notesscroller.stream = self.knownNotesstream
        #print "len(ret) " + str(len(ScreenState["OlgaViewChallengeScreen"].notesscroller.song.mystream))
        ScreenState["OlgaViewChallengeScreen"].dirty = True
        ScreenState.change_state("OlgaViewChallengeScreen")
        return

        pass

    def playChallenge(self):
        stream=self.knownNotesstream
        speed=1.0
        output = myglobals.gameState.myMidiController.getMidiOut()
        output.playpartMyStream(stream , 0 , len(stream), startnote=stream.notes[0],speed=speed)


    def SetChallenge(self):
        ScreenState["ConfigAChallengeStreamScreen"].notesscroller.stream = self.song.mystream
        #ScreenState["ConfigAChallengeStreamScreen"].song = myglobals.gameState.song

        ScreenState.change_state("ConfigAChallengeStreamScreen")
        #ScreenState["ConfigAChallengeScreen"].dirty = True
        pass


    def ConfigChallenge(instance=None):
        ScreenState.change_state("ConfigOlgaOptionsScreen")


    def ShowRun(self,v):
        pass