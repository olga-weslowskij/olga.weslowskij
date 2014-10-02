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
from Game import options
#from Game.chordReport import ChordReport
from Game.myLogHandler import infoLog
from Game.myRunStateChallengeSimon import MyRunStateChallengeSimon

from Game.myKey import mykey
from Game.myJumpChordsAndSpeedTols import MyJumpChordsAndSpeedTols
#from myLevenshteinChallengeSimon import MyRunStateChallengeSimon
from Game.mySong import MySong
from Game.myStream import MyStream, ischordms
import myglobals


logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

class AllYouProofedYouCanPlay(object):
    def getNewPartstartNote(self, asong, aKnownNote):
        #return asong.getLevelStartNote(aKnownNote)
        if aKnownNote.lastChord:
            return aKnownNote.lastChord.notes[0]
        else:
            # start
            return aKnownNote.notes[0]

        pass

    def getNewPartendNote(self, asong, aKnownNote):
        #return asong.getLevelEndNote(aKnownNote)
        #return asong.getLevelStartNote(aKnownNote).chord.notes[-1]

        if aKnownNote.lastChord:
            return aKnownNote.lastChord.notes[-1]
        else:
            # start
            return aKnownNote.notes[-1]
        #return aKnownNote.lastChord.notes[-1]
        pass


allyouproofedyoucanplay = AllYouProofedYouCanPlay()



class SimonModeChallengeFeedback(object):
    def __init__(self):

        self.song=MySong()
        self.speed=None

        self.knownNotesstream = MyJumpChordsAndSpeedTols()

        self.challenge=None
        self.newpart = None
        self.oldpart = None

        # prestart is SongPartStart
        self.adaptiveStart=True

        self.oldbestActiveAbsError = None
        self.newbestActiveAbsError = None

        self.doneRun=None


        #self.challenge=None

        #myglobals.SimonMode = self

        self.startchord= None
        self.endchord = None
        self.songpart=None
        self._phase=-1

    @property
    def phase(self):
        return self._phase


    @phase.setter
    def phase(self, value):
        if self.phase != value:
            logger.info("Phase change " + str(value))
            if value == 4:
                #myglobals.FeedBack.playGoodMelodie()
                pass

            if value == 0:
                # TODO can we have one speed value?
                if self.speed:
                    aspeed =1/self.speed
                else:
                    aspeed=1.0
                myglobals.FeedBack.playOnPause(self.allpart, speed = aspeed)
                infoLog.log("a new challenge")


        self._phase=value



    def createSimpleChallenge(self):

        logger.info("Simon create Challenge  " + str(self.startchord) +" -  " + str(self.endchord))


        newstart= self.startchord
        levelend = self.endchord

        self.allpart = MyStream()
        self.allpart = self.allpart.buildAllInChordRange(newstart,levelend)
        self.allpart = self.allpart.decorate()


        #self.challenge=MyLevenshteinChallengeAbsError()
        #self.challenge=MyLevenshteinChallengeOlga()
        self.challenge=MyRunStateChallengeSimon()

        #self.challenge=MyLevenshteinChallengeOlga()


        newstart= self.allpart[0]
        levelend = self.allpart[-1]

        # forced entry for errors??
        self.challenge.challengestartnote=newstart


        # needed for challenge.knownStream
        self.challenge.challengeendchord=levelend.chord

        self.targetall = (None, levelend.chord)

        self.challenge.targets=[self.targetall]

        """
        # build appends and unpacks notes so destroys decorate
        # we want to work with pointer notes to WorldSongStream
        self.prepart = MyStream()
        self.prepart.build(prestart, newstart)
        self.prepart = self.prepart.decorate()
        """


        # create prestarts
        #self.challenge.setStartNote(newstart)
        #self.challenge.setStartStream([newstart])
        self.challenge.setStartSelection([newstart])


        self.challenge.maxerror=[0,0]

        for x in self.allpart:
            self.challenge.maxerrorAtKnownnote[x] = [0,0]

        self.challenge.speedtol = 0.0

        self.tnewstart=None

        self.longesttime = None

        self._phase =- 1



    def configStartAndEndStreams(self):

        #logger.info("Simon set start " + str(inaKnownNote))
        logger.info("Simon set start " + self.startchord.prettyprint() + " " + str(self.songpart))

        #

        newpartstart= allyouproofedyoucanplay.getNewPartstartNote(self.song, self.startchord)


        #self.songpartstart = self.song.getLevelStartNote(aKnownNote.notes[0]).chord
        self.songpartstart = self.song.getLevelStartNoteNr(self.songpart).chord

        logger.info("self.adaptiveStart: " + str(self.adaptiveStart))
        if self.adaptiveStart:
            # fast progress, needs more cpu at the moment
            prestart = self.song.getLevelStartNote(self.startchord.notes[0])

            prestart = self.song.getLevelStartNoteNr(self.songpart)
            logger.info("self.songpart: " + str(self.songpart) + ": " + str(prestart))
        else:
            # no fast progress, strict, pure lectures
            prestart=newpartstart


        newpartend = allyouproofedyoucanplay.getNewPartendNote(self.song, self.startchord)

        #levelend = self.song.getLevelEndNote(aKnownNote.notes[0])
        levelend = self.song.getLevelEndNoteNr(self.songpart)

        levelend = levelend.chord.notes[-1]

        self.endchord = levelend.chord

        #levelend = self.song.mystream.notes[750]
        #levelend = self.song.mystream.notes[-1]
        #levelend =self.knownNotesstream.notes[-1]

        #self.challenge=MyLevenshteinChallenge()
        #self.challenge.challengestartnote=newpartstart

        logger.info("prestart " + str(prestart))
        logger.info("newpartstart " + str(newpartstart))
        logger.info("newpartend " + str(newpartend))
        logger.info("levelend " + str(levelend))

        #self.challenge=MyLevenshteinChallengeAbsError()
        #self.challenge=MyLevenshteinChallengeOlga()
        self.challenge=MyRunStateChallengeSimon()


        # forced entry for errors??
        self.challenge.challengestartnote=newpartstart


        # needed for challenge.knownStream
        self.challenge.challengeendchord=self.endchord

        self.targetnewpart = ("Never", newpartend.chord)
        self.targetall = ("Never", self.endchord)

        self.targetnewpart = newpartend.chord
        self.targetall = self.endchord

        self.challenge.targets=[self.targetnewpart,self.targetall]

        logger.info("targets " + str(self.challenge.targets))

        """
        # build appends and unpacks notes so destroys decorate
        # we want to work with pointer notes to WorldSongStream
        self.prepart = MyStream()
        self.prepart.build(prestart, newpartstart)
        self.prepart = self.prepart.decorate()
        """

        # prepart us used as entry and needs decoration beyond end of prepart

        #self.prepart = self.song.mystream.buildList(prestart, newpartstart)

        self.prepart = self.song.mystream.buildAllInChordRangeList(prestart, newpartstart)


        self.olgapartStream= MyStream()
        # missing last note in display prepart
        #self.olgapartStream.build(prestart,levelend)
        self.olgapartStream = self.olgapartStream.buildAllInChordRange(prestart,levelend)
        logger.info("olgaPartStreamEnd " + str(self.olgapartStream[-1]))
        self.olgapartStream = self.olgapartStream.decorate()
        logger.info("olgaPartStreamEnd after decorate " + str(self.olgapartStream[-1]))

        #self.olgapartList = self.song.mystream.buildList(prestart, levelend)
        self.olgapartList = self.song.mystream.buildAllInChordRangeList(prestart, levelend)

        self.newpart = MyStream()
        self.newpart.build(newpartstart,newpartend)
        self.newpart = self.newpart.decorate()


        self.allpart = MyStream()
        self.allpart = self.allpart.buildAllInChordRange(newpartstart,levelend)
        self.allpart = self.allpart.decorate()


        # create prestarts
        #self.challenge.setStartNote(newpartstart)
        #self.challenge.setStartStream(self.prepart)
        self.challenge.setStartSelection(self.prepart, myglobals.SimonMode.speed, myglobals.SimonMode.speedtol)


        self.oldpart = MyStream()

        if hasattr(newpartend,"next"):
            if newpartend.next:
                self.oldpart.build(newpartend.next,levelend)
            else:
                self.oldpart.build(newpartend,levelend)
        else:
                self.oldpart.build(newpartend,levelend)

        # default, needed for prestart

        # dangerouse prepart is worldsongstream
        # newpart and oldpart new Streams and new decorations
        # i dont know if this works
        # so expect no errorcutting when you raise global maxerror

        self.challenge.maxerror=[0,0]

        for x in self.prepart:
            self.challenge.maxerrorAtKnownnote[x] = [0,0]

        for x in self.newpart:
            self.challenge.maxerrorAtKnownnote[x] = [0,0]

        for x in self.oldpart:
            self.challenge.maxerrorAtKnownnote[x] = [0,0]


        self.challenge.speedtol = 0.0
        # double speedtol widget olga builds last so it reads that value
        #self.challenge.speedtol = options.getOptionValue("speedtol")
        self.challenge.speedtol = myglobals.SimonMode.speedtol

        #print "self.challenge.speedtol ", self.challenge.speedtol


        self.tnewstart=None
        self.rtnewstart=None

        self.longesttime = None

        myglobals.ScreenState["Simon"].levcha = self.challenge
        myglobals.ScreenState["Simon"].dirty = True

        #self.chordreport = ChordReport(None)

        self.oldbestActiveAbsError = None
        self.newbestActiveAbsError = None

        self._phase=-1


    def solcmp(self, a):
        return (self.challenge.seen[a][0:2], a.lastjumpRun.getKnownChord().pos)


    def activeChallenge(self):
        return self.challenge

    def update(self, aNote, aTime):
        #ScreenState["Song"].levcha2 = self.challenge
        #ScreenState["Song"].levcha = self.challenge

        # init
        #if self.challenge is None or self.challenge is None:
        if self.challenge is None:
            if self.song is None:
                return
            else:
                logger.info("init update")
                # addSong decorates

                #tmp = self.knownNotesstream.addSong(self.song,options.getOptionValue("hand"))
                tmp = self.knownNotesstream.registerStream(self.song.mystream, myglobals.SimonMode.speed, myglobals.SimonMode.speedtol)

                self.song.mystream = tmp
                if  len(tmp) > 0:
                    self.startchord=tmp.notes[-1].chord
                    self.configStartAndEndStreams()
                #self.setStartNote(self.song.mystream.notes[-1])

        # init failed
        # if self.challenge is None or self.challenge is None:
        if self.challenge is None:
            return

        if len(self.challenge.donelist.get(self.targetnewpart,[])) == 0:
            self.phase=0

        #if options.getOptionValue("mode") == "simon":
        if True:
            if aNote is None:
                #self.challenge.update()
                #self.challenge.update()
                self.challenge.updatePause(aTime)
                pass

            if aNote:
                #self.chordreport = ChordReport(aNote)
                #self.chordreport = myglobals.SimonMode.getChordReport(aNote)
                self.challenge.add_note(aNote)


                #self.oldfarestAvtive=self.challenge.farestActive()


                #logger.info("self.oldfarestAvtive "+ str(self.oldfarestAvtive))

                #if self.challenge.bestabsrun:
                if False:
                    self.oldbestActiveAbsError = self.challenge.computeAbsError(self.challenge.bestabsrun)
                else:
                    self.oldbestActiveAbsError = mykey([0,0])


                logger.debug("self.oldBestError "+ str(self.oldbestActiveAbsError))

                #self.challenge.add_note(aNote)

                self.challenge.update()

                if False:
                    self.newbestActiveAbsError = self.challenge.computeAbsError(self.challenge.bestabsrun)
                    logger.debug("self.newBestError "+ str(self.newbestActiveAbsError))
                else:
                    self.newbestActiveAbsError = mykey([0,0])



                #self.challenge.update()
                self.longesttime = None

                #self.challenge.draw()

            #check

                #if len(self.challenge.donelist) == 0:
                # newparts
                # check newpart done


                if len(self.challenge.donelist.get(self.targetnewpart,[])) == 0:
                    # done already?
                    # self.phase=0
                    """
                    # todo Fix estimate to target
                    if self.oldbestActiveAbsError:
                        if self.newbestActiveAbsError:
                            if self.newbestActiveAbsError[0:2] > self.oldbestActiveAbsError[0:2]:
                                logger.debug("phase 0 " + str(self.newbestActiveAbsError[0:2]) +" > " + str(self.oldbestActiveAbsError[0:2]))
                                logger.debug(type(self.newbestActiveAbsError[0:2]))

                                # non increasing prestart
                                self.chordreport.decreasingBestLenMaps = True
                            else:
                                self.chordreport.decreasingBestLenMaps = False
                                self.chordreport.noactiveMap= False
                    else:
                        if self.newbestActiveAbsError > 0:
                            self.chordreport.decreasingBestLenMaps = True
                        else:
                            self.chordreport.decreasingBestLenMaps = False
                            self.chordreport.noactiveMap= False
                    """


                else:
                    if self.phase == 0:
                        #play good melody phase 0
                        #self.chordreport.challengedone=True
                        self.phase = 1


                    #logger.info("newpart done " + str(self.challenge.donelist.get(self.targetnewpart,[])))
                    logger.debug("newpart done ")
                    #if len(self.challenge.donelist)>= int(options.getOptionValue("repeat")):

                    targetalldones =self.challenge.donelist.get(self.targetall,[])

                    if len(targetalldones)> 0:
                        logger.debug("combined done ")#+ str(self.challenge.donelist))

                        if self.phase==1:
                            self.phase = 2

                        #self.chordreport.challengedone=True

                        #createShowDoneStream(None)

                        #tnewstart =min(self.challenge.donelist[self.targetall],key = lambda  a: (self.challenge.seen[a],len(a.list)))
                        #tnewstart =min(self.challenge.donelist[self.targetall],key = lambda  a: (self.challenge.seen[a],a.lenlist))
                        #tnewstart =min(self.challenge.donelist[self.targetall],key = lambda  a: (self.challenge.seen[a],a.lastjumpRun.lenlist))
                        logger.info("len(targetalldones) " + str(len(targetalldones)))
                        for sol in targetalldones:
                            logger.info(sol.lastjumpRun.prettyprint())
                            logger.info(sol.prettyprint())
                            logger.info("\n")



                        tnewstart =min(targetalldones,key = self.solcmp)

                        logger.info("tnewstart pos "+ str(tnewstart.lastjumpRun.getKnownChord().pos))
                        #logger.info("tnewstart offset "+ str(tnewstart.lastjumpRun.currentMelodyRating.notenextMapping.knownChord[0].myoffset))
                        #logger.info("tnewstart "+ tnewstart.prettyprint())


                        # No we want to end this challenge with a pause
                        if False:

                            # wait for best
                            if self.tnewstart is not None and self.tnewstart is tnewstart:
                                logger.info("combined done and not improving "+ str(self.challenge.donelist[self.targetall]))
                                self.phase = 4
                                #play good melody

                                myglobals.FeedBack.playOnPause(myglobals.FeedBack.goodmelodie.mystream)


                                # create next challenge

                                self.newstart =self.tnewstart.list[1].notenextMapping.knownChord

                                #logger.info("self.newstart "+ str(self.newstart))
                                logger.info("self.newstart "+ self.newstart.prettyprint())

                                # self.setStartNote(newstart)
                                # self.tnewstart = None
                                # play new challenge
                            else:
                                self.tnewstart = tnewstart
                                # new challenge starts at
                                self.newstart = self.tnewstart.list[1].notenextMapping.knownChord

                        else:
                            #self.tnewstart =min([self.tnewstart,tnewstart],key = self.solcmp)
                            self.tnewstart = tnewstart
                            self.challenge.donelist.get(self.targetall,[]).remove(self.tnewstart)


                        #code.interact(local=locals())

                    else:
                        logger.debug("combined not done ")
                        # challenge not done yet


                    #logger.info("self.oldfarestAvtive")
                    #logger.info(str(self.oldfarestAvtive))
                    #logger.info(str(self.challenge.farestActive()))

                    """
                    if self.oldbestActiveAbsError:
                        if self.newbestActiveAbsError:
                            if self.newbestActiveAbsError[0:2] > self.oldbestActiveAbsError[0:2]:
                                # non increasing prestart
                                self.chordreport.decreasingBestLenMaps = True
                            else:
                                self.chordreport.decreasingBestLenMaps = False
                                self.chordreport.noactiveMap= False
                    else:
                        if self.newbestActiveAbsError > 0:
                            self.chordreport.decreasingBestLenMaps = True
                        else:
                            self.chordreport.decreasingBestLenMaps = False
                            self.chordreport.noactiveMap= False
                    """



                #myglobals.FeedBack.update(self.chordreport)

            else:
                # no note
                #check future Timingerror and pause
                #if self.challenge.checkFutureTimmingError(aTime):
                self.challenge.updatePause(aTime)
                """
                if False:
                    if self.phase ==0:
                        self.chordreport.timingfail = True
                    logger.info("simon future speedtol fail\n")
                """


                #if self.challenge.checkPause(aTime):
                if self.challenge.paused:
                    # newtry
                    #self.chordreport.newtry = True
                    #logger.info("Pause\n")

                    pass

                # all done we are waiting for a nice one and a pause
                if self.phase >= 2:
                    self.oldfarestAvtive=None
                    # no candidate
                    if self.tnewstart:
                        # pause detection based on currentMelodyRating
                        # failed pause at the end of challenge
                        In = self.tnewstart.getInNote()
                        if hasattr(In, "next") and ischordms > In.next.myoffset-In.myoffset:
                            logger.info("no time after challenge! " + self.tnewstart.prettyprint())
                            logger.info("In , In.next " + In.prettyprint() + In.next.prettyprint())
                            self.tnewstart = None
                            #self.phase = 1
                            return

                        #if self.tnewstart.nextKnownNoteDeltaTimeLastGood() is None or self.tnewstart.nextKnownNoteDeltaTimeLastGood() / (self.tnewstart.rspeed()-(self.challenge.speedtol)) < aTime - self.tnewstart.lastAllGoodRunMelodyRating.notenextMapping.innote.myoffset:
                        if ischordms <= aTime - In.myoffset:
                            try:
                                #logger.info("combined done and pause times " + str(self.tnewstart.nextKnownNoteDeltaTimeLastGood()) +"/"+ str( (self.tnewstart.rspeed()-(self.challenge.speedtol))) +" < " +str(aTime) + " - " +  str(self.tnewstart.lastAllGoodRunMelodyRating.notenextMapping.innote.myoffset))
                                logger.info("combined done and small pause " + str(ischordms) + "< "+ str(aTime-In.myoffset ))
                            except:
                                pass

                            if self.phase < 3:
                                myglobals.FeedBack.playOnPause(myglobals.FeedBack.goodmelodie.mystream)
                                infoLog.log("Da, well done")
                                self.phase = 3

                            # find better solution
                            if self.rtnewstart:
                                logger.info("comparing possible solutions " + str(map(self.solcmp, [self.tnewstart,self.rtnewstart])))
                                self.rtnewstart =min([self.tnewstart,self.rtnewstart],key = self.solcmp)
                                logger.info("picking pos "+ str(self.rtnewstart.lastjumpRun.getKnownChord().pos))

                            else:
                                self.rtnewstart= self.tnewstart
                            self.tnewstart = None

                        #createShowDoneStream(None)

                #if self.phase == 3 and self.challenge.checkPause(self.rtnewstart):
                    if self.rtnewstart:
                        #logger.info("waiting for pause " + str(self.challenge.paused))
                        if self.phase == 3 and self.challenge.paused and True:
                            self.phase = 4
                            #play good melody

                            # create next challenge
                            # newstart = self.tnewstart.list[1].notenextMapping.knownote

                            #self.newstart = self.rtnewstart.firstRunMelodyRating.getKnownChord()

                            self.doneRun = self.rtnewstart
                            self.newstart = self.rtnewstart.lastjumpRun.getKnownChord()
                            #logger.info("self.newstart "+ str(self.newstart))


                            logger.info (str(self.newstart) +" == " + str(self.songpartstart))
                            if self.newstart == self.songpartstart:
                                infoLog.log("Da, this part was good")
                                logger.info("A PART COMPLETED\n")


                            logger.info("self.newstart "+ self.newstart.prettyprint())
                            logger.info("pos "+ str(self.rtnewstart.lastjumpRun.getKnownChord().pos))
                            # self.setStartNote(newstart)
                            if logger.isEnabledFor(logging.INFO):
                                #logger.info("combined done and pause " + self.rtnewstart.prettyprint())
                                logger.info("combined done and BIG pause ")

                            #code.interact(local=locals())
                            self.tnewstart=None
                            self.rtnewstart = None











