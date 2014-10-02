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
#from myLevenshteinChallengeOlga import MyLevenshteinChallengeOlga
from Game.myJumpChordsAndSpeedTols import MyJumpChordsAndSpeedTols
from Game.myLogHandler import infoLog
from Game.myRunStateChallengeOlga import MyRunStateChallengeOlga
from Game.mySong import MySong
import myglobals

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
#logger.setLevel(logging.NOTSET)
logger.setLevel(logging.INFO)


class OlgaMode(object):


    def __init__(self):
        #self.song=MySong()
        myglobals.OlgaMode = self
        self.challenge = None

        self.uptime=None

        #self.reportederrors={}

        self.paused = False

    # wow i hope im wrong:
    # redefine a "proberty setter" only would require me to write a getter, init a _variable
    # and this function
    # i like to define a property and just change the setter
    # even better just write a property.setter method to declare a property


    def setknownNotesstream(self, s, aspeed, aspeedtol):
        if logger.isEnabledFor(logging.INFO):
            try:
                logger.info("setknownNotesstream\n" + s.prettyprint())
            except:
                logger.info("setknownNotesstream\n" + str(s))
        #print "setknownNotesstream "+ s.prettyprint() +"\n"

        # new challenge clears all running runs too ...
        #self.challenge = MyLevenshteinChallengeOlga()
        if self.challenge is None:
            self.challenge = MyRunStateChallengeOlga()

        self.challenge.jumpToStates = MyJumpChordsAndSpeedTols()

        # self.challenge.jumpToStates.addSong(s.song, options.getOptionValue("hand"))


        # just to decorade ..
        #sdec = self.challenge.jumpToStates.addStream(s)

        sdec = self.challenge.jumpToStates.registerStream(s, aspeed, aspeedtol)
        #self.challenge.setStartSelection(s)


        """
        self.knownNotesstream = s

        self.challenge.setStartSelection(s)
        """

        #self.challenge.speedtol=0.5
        #self.challenge.verbosetimming=True
        #print len(self.challenge.jumpToStates)


    def checkPause(self, atime):
        return self.challenge.checkPaused(atime)


    def update(self, aNote, aTime):
        if self.paused == False:
            if aTime:
                self.uptime=aTime
            if aNote:
                self.uptime=aNote.myoffset

            if self.challenge:
                #logger.debug("update Olga " + str(self.challenge.speedtol))
                #logger.info("update Olga " + str(self.challenge.speedtol))

                """
                if self.challenge.initdone is False:
                    # init
                    self.challenge.myinit()
                """


                if aTime:
                    self.challenge.updatePause(aTime)

                if aNote:
                    self.challenge.add_note(aNote)
                    self.challenge.update()


                if (self.challenge.bestActive()):
                    r = self.challenge.bestActive()
                    #mr = r.list[-1]

                    # we need to search
                    # only the last 2?

                    if r.lastRunState and len(r.lastRunState.errors) > 0:
                        mr = r.lastRunState.errors[0]
                        if  mr.feedbacktime is None:
                            mr.giveFeedback(myglobals.FeedBack)
                            infoLog.error(mr.derrorstr)
                            if logger.isEnabledFor(logging.INFO):
                                logger.info(r.lastRunState.prettyprint())

                        if logger.isEnabledFor(logging.INFO):
                            for error in r.errors:
                                logger.info(error.derrorstr)


                    if len(r.errors) > 0:
                        mr = r.errors[0]
                        if  mr.feedbacktime is None:
                            mr.giveFeedback(myglobals.FeedBack)
                            infoLog.error(mr.derrorstr)
                            if logger.isEnabledFor(logging.INFO):
                                logger.info(r.prettyprint())





