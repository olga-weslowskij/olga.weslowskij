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
from collections import OrderedDict
#from myChallenge import MyChallenge
from Game import options
#from Game.chordReport import ChordReport
from Game.myJumpChordsAndSpeedTols import MyJumpChordsAndSpeedTols
from Game.myLogHandler import infoLog
import myglobals

import logging
from Game.simonModeChallengeFeedback import SimonModeChallengeFeedback, allyouproofedyoucanplay
from mylibs.myList import MyList
from mylibs.myPersistent import PersistentObject

logger = logging.getLogger('SimonMode')
hdlr = logging.FileHandler('./SimonMode.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)


class SimonMode(PersistentObject):
    def __init__(self):
        self.song=None
        #self.knownNotesstream = myStartRuns()
        myglobals.SimonMode = self


        self.simonModeChallenges=MyList()

        self.simonModeChallengesactive=MyList()
        self.simonModeChallengesactiveRising=MyList()
        self.simonModeChallengesdones=OrderedDict()

        self.speedtol=0.0
        self.speed=None
        self.startchord=None
        self.songpart=None
        self.repeat=1
        self.adaptive = False

        self.config = False

        self.paused = False





        self.nid=None

        super(SimonMode,self).__init__()

        #self.persistentattr=["speedtol", "speed", "repeat", "adaptive","startchord"]
        self.persistentattr=["speedtol", "speed", "repeat", "adaptive", "paused", "songpart"]

        self.showattr = ["speedtol", "speed", "repeat", "adaptive", "paused", "startchord", "songpart", "initSimonChallenges"]

        try:
            self.fromXml2file(self.__class__.__name__+".xml")
        except:
            self.nid=myglobals.persistent.getId()
            pass


    def initSimonChallenges(self, astartNote=None, speedtol=None):

        infoLog.log("Hello, Im Olga, lets start some lectures: listen me first, then replay")


        if self.song:
            if self.startchord is None:
                self.startchord=self.song.mystream[-1].chord

            if self.songpart is None:
                self.songpart = len(self.song.endparts) #-1


        if speedtol:
            self.speedtol=speedtol

        self.simonModeChallenges=MyList()

        self.simonModeChallengesactive=MyList()
        self.simonModeChallengesactiveRising=MyList()
        self.simonModeChallengesdones=OrderedDict()

        ret = SimonModeChallengeFeedback()
        ret.song = self.song


        #dec = ret.knownNotesstream.addSong(self.song, self.song.handparts)
        #ret.song.mystream = dec

        ret.songpart = self.songpart


        # startchord should be in songpart
        if self.song.getLevelEndNoteNr(self.songpart).myoffset < self.startchord.myoffset:
            self.startchord = self.song.getLevelEndNoteNr(self.songpart).chord
        if self.song.getLevelStartNoteNr(self.songpart).myoffset > self.startchord.myoffset:
            self.startchord = self.song.getLevelEndNoteNr(self.songpart).chord

        #ret.setStartNote()
        if astartNote:
            ret.newstart=astartNote.chord

        else:
            #ret.newstart=allyouproofedyoucanplay.getNewPartendNote(ret.song, ret.song.mystream[-1].chord)
            #ret.newstart=ret.song.mystream[-1].chord
            ret.newstart= self.startchord




        #self.simonModeChallengesdones.append(ret)
        # fake init and set last done ???
        #self.simonModeChallengesdones[ret]=ret

        # instructing Olga
        #myglobals.OlgaMode.challenge.setStartStream(ret.allpart)

        if self.song:
            self.config = True


        self.toXml2file(self.__class__.__name__+".xml")

    """
    def getChordReport(self, aNote):
        if self.chordreports.get(aNote,None) is None:
            self.chordreports[aNote] = ChordReport(aNote)
            if aNote:
                self.chordreports[aNote].noactiveMap = True

        return self.chordreports[aNote]
    """


    def update(self, aNote, aTime):
        """
        # init per createchallenge
        if len(self.simonModeChallengesdones) == 0:
            return
        """
        if self.config is False:
            return

        if self.paused:
            return

        active=MyList()
        self.simonModeChallengesactiveRising = MyList()


        for x in self.simonModeChallengesactive:
            # 2 sets olga to new challenge so you cant play past the end
            #if x.phase < 2:
            if x.phase < 4:
                self.simonModeChallengesactiveRising.append(x)
            else:
                # not working cause of fake  just 1 challeneg history
                #self.simonModeChallengesdones.clear()
                #self.simonModeChallengesdones.append(x)

                self.simonModeChallengesdones[x]=x
                #createShowDoneStream(None)
            if x.phase < 4:
                if aNote:
                    #gu.logger.info("Simon updates a Note on \n" + x.startchord.prettyprint() + ": " + aNote.prettyprint())
                    pass
                active.append(x)
                x.update(aNote,aTime)


        self.simonModeChallengesactive = active


        #if len(self.simonModeChallengesactiveRising) == 0:
        # why do we need 2 active simonchallenges anyway?????
        # keyboard gesture detection, playPartdction
        # pause is input ....
        if len(self.simonModeChallengesactive) == 0:
            if len(self.simonModeChallenges) == 0:
                # create new challenges
                # improve me

                #x = self.simonModeChallengesdones[-1]

                # start at last done challenge
                if len(self.simonModeChallengesdones) > 0:
                    x = self.simonModeChallengesdones.popitem()[1]
                    self.simonModeChallengesdones[x]=x
                    self.startchord = x.newstart
                    #self.songpart = self.song.getLevelPos(self.startchord[0])
                    if self.startchord == self.song.getLevelStartNoteNr(self.songpart).chord:
                        self.songpart = max(0,x.songpart-1)


                #for y in range(int(options.getOptionValue("repeat"))):
                for y in range(self.repeat):
                    nc = SimonModeChallengeFeedback()
                    nc.adaptiveStart = self.adaptive
                    nc.song = self.song
                    nc.startchord = self.startchord
                    nc.songpart=self.songpart
                    nc.configStartAndEndStreams()
                    nc.speed = self.speed
                    nc.speedtol = self.speedtol



                    # double speedtol widget olga builds last so it reads that value
                    #nc.activeChallenge().speedtol= options.getOptionValue("speedtol")
                    self.simonModeChallenges.append(nc)

            tmp = self.simonModeChallenges.pop()
            #self.simonModeChallengesactiveRising.append(tmp)
            self.simonModeChallengesactive.append(tmp)

            #myglobals.FeedBack.challenges.append(tmp.activeChallenge())

            #gu.logger.info("Simon sets active challenge\n" + tmp.allpart.prettyprint())

            # inform Olga
            #myglobals.OlgaMode.challenge.setStartStream(nc.song.mystream)
            #myglobals.OlgaMode.challenge.setStartStream(tmp.allpart)
            #myglobals.OlgaMode.setknownNotesstream(tmp.allpart)
            myglobals.OlgaMode.setknownNotesstream(tmp.olgapartList, tmp.speed, tmp.speedtol)
            # TODODone
            # BAD Setting speedtol for all
            # myStartRuns should be RunStates with timmings..
            # Olga should be able to handle multiple Challenges
            # myglobals.OlgaMode.challenge.speedtol = tmp.activeChallenge().speedtol

            # play challenge


        # TODOne dont belong here
        #myglobals.FeedBack.update(self.getChordReport(aNote))



    def lastDoneChallenge(self):
        if len(self.simonModeChallengesdones) == 0:
            return None
        x = self.simonModeChallengesdones.popitem()[0]
        self.simonModeChallengesdones[x]=x
        return x

    def activeChallenge(self):
        if (len(self.simonModeChallengesactiveRising) > 0):
            return self.simonModeChallengesactiveRising[-1]

        if (len(self.simonModeChallengesactive) > 0):
            return self.simonModeChallengesactive[-1]

        return None


    pass

