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
from myglobals import ScreenState
from Game.myStream import MyStream
import myglobals
#import gameEngineRoot
import logging

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ +  '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)



def SetChallenge():
    ScreenState["ConfigAChallengeStreamScreen"].notesscroller.stream = myglobals.gameState.song.mystream
    ScreenState["ConfigAChallengeStreamScreen"].challenge = myglobals.OlgaMode.challenge
    #ScreenState["ConfigAChallengeStreamScreen"].song = myglobals.gameState.song

    ScreenState.change_state("ConfigAChallengeStreamScreen")
    #ScreenState["ConfigAChallengeScreen"].dirty = True
    pass


def ConfigChallenge(instance=None):
    ScreenState.change_state("ConfigOlgaOptionsScreen")



def ShowChallenge():
    print "ShowChallenge\n"
    logger.debug("enter ShowChallenge\n")
    #levcha = MyLevenshteinChallenge()
    #levcha = ScreenState["Song"].levcha2
    if len(myglobals.OlgaMode.challenge.jumpToStates.knownStreams) == 0:
        logger.debug("no stream\n")
        print "no stream\n"
        ret = MyStream()
        return ret

    logger.debug("stream done\n")
    print "stream done\n"

    #code.interact(local=locals())

    ret = myglobals.OlgaMode.challenge.jumpToStates.knownStreams[0]
    #ret.build(start, end)
    #ret = ret.chordify()
    #print "len(ret) " + str(len(myglobals.OlgaMode.knownNotesstream.song.mystream))
    print "len(ret) " + str(len(ret))

    # "OlgaViewChallengeScreen"
    ScreenState["OlgaViewChallengeScreen"].notesscroller.stream = ret
    #print "len(ret) " + str(len(ScreenState["OlgaViewChallengeScreen"].notesscroller.song.mystream))
    ScreenState["OlgaViewChallengeScreen"].dirty = True
    ScreenState.change_state("OlgaViewChallengeScreen")
    return ret

def playChallenge():
    #end = myglobals.SimonMode.activeChallenge().challenge.challengeendnote
    #end = myglobals.SimonMode.activeChallenge().challenge.challengeendnote
    #start = myglobals.SimonMode.activeChallenge().challenge.challengestartnote

    #ret = MyStream()
    #ret.build(start, end)

    #ret = myglobals.SimonMode.activeChallenge().challenge.knownStream()
    ret = myglobals.OlgaMode.knownNotesstream

    stream=ret
    speed=1.0
    output = myglobals.gameState.myMidiController.getMidiOut()
    output.playpartMyStream(stream , 0 , len(stream), startnote=stream.notes[0],speed=speed)