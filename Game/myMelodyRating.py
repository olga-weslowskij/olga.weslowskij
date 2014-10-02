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
from Game.myKey import mykey
from Game.myKnownChord import theUnknownChord
from Game.mySong import MySong

from Game.myStream import ischordms
import myglobals

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ +  '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)
#logger.setLevel(logging.DEBUG)



class ErrorFeedBack(object):
    def __init__(self, *args, **kwargs):
        #MelodyRating.__init__(self, *args, **kwargs)
        self.feedbacktime=None
        self.costs = mykey([0])
        self.errorstr=self.__class__.__name__
        self.derrorstr=self.__class__.__name__


    def giveFeedback(self, output):
        logger.info("Giving Feedback for error: " + self.errorstr)
        self.feedbacktime=myglobals.gameState.getMidiTick()

    def __str__(self):
        return self.errorstr

    def check(self, aRunStateRun):
        pass



class Missed(ErrorFeedBack):
    def __init__(self, *args, **kwargs):
        ErrorFeedBack.__init__(self, *args, **kwargs)
        self.errorstr=self.__class__.__name__




class Wrong(ErrorFeedBack):
    def __init__(self, *args, **kwargs):
        ErrorFeedBack.__init__(self, *args, **kwargs)
        self.errorstr=self.__class__.__name__
        self.costs = mykey([1])

    def giveFeedback(self, output):
        ErrorFeedBack.giveFeedback(self, output)
        output.playMelodieError(polite=False)
        #output.playMelodieError(polite=True)
        self.feedbacktime=myglobals.gameState.getMidiTick()


class KnChordInTimeTooLate(ErrorFeedBack):
    def __init__(self, *args, **kwargs):
        ErrorFeedBack.__init__(self, *args, **kwargs)
        self.errorstr=self.__class__.__name__
        self.costs = mykey([1,1])

        #self.costs = mykey([0,1])

    def giveFeedback(self, output):
        ErrorFeedBack.giveFeedback(self, output)
        #output.playTimingError(polite=True)
        output.playMelodieError(polite=True)
        self.feedbacktime=myglobals.gameState.getMidiTick()
    
    def check(self, aRunState, atime=None):
        if not(aRunState is None):
            if not (aRunState.knownChordInNoteMap is None):
                di = abs(atime - aRunState.knownChordInNoteMap.innote.myoffset)
                firstchord = aRunState.getKnownChord()
                secondchord = aRunState.knownChordInNoteMap.activeKnownChord()

                # bad dk is given and should not be aprox by ischordms
                #if dk < ischordms:
                #if aRunState.knownChordInNoteMap.knownChord.pos == aRunState.lastRunState.knownChord.pos:

                if firstchord:
                    if firstchord is secondchord and aRunState.lastjumpRun == aRunState.lastRunState.lastjumpRun:
                        # run speed dependend?
                        #if di * max(1,aRunState.rspeed(d=1))< ischordms:
                        #or  abs
                        if di < ischordms:

                            # nice in Chord
                            #aRunState.errorstr = "nice in Chord Timing"
                            pass
                        else:
                            # Timming error
                            #self.errorstr = "Kn Chord, In no Chord Timing"


                            cmap = aRunState.getKnownChordInNoteMap()
                            try:
                                sk = ""
                                for n in cmap._knownChord:
                                    if n not in cmap.playedChordNotesgood:
                                        if len(sk) > 0:
                                            sk = sk +", " + (n.noteName())
                                        else:
                                            sk = sk + " " + (n.noteName())

                            except Exception as e:
                                #print(e)
                                sk = ""
                                pass
                            self.errorstr = sk + " missing"

                            if aRunState.rspeed(d=1) is None:
                                print "aRunState.rspeed(d=1) is None"
                                1/0

                            self.derrorstr = "di * aRunState.rspeed(d=1)< ischordms\n" + " ".join(map(str,[atime,aRunState.knownChordInNoteMap.innote.myoffset,di,aRunState.rspeed(d=1),ischordms]))
                            #self.derrorstr += "\n" + str(firstchord) + "\n" +str(secondchord)
                            #self.derrorstr += "\n" + str(aRunState.getKnownChordInNoteMap().chordfull())
                            self.derrorstr += "\n" + str(aRunState.getKnownChordInNoteMap().prettyprint())

                            try:
                                self.derrorstr += "\n" + str(aRunState.getInNote().next)
                            except:
                                self.derrorstr += "\n" + str(aRunState.getInNote().__dict__)



                            #self.errorstr = self.derrorstr


                            #aRunState.errorstr = aRunState.errorstr + " " + str(di * aRunState.rspeed(d=1)) + " < " + str(ischordms) + " " +str(aRunState.rspeed(d=1))
                            #aRunState.errorstr = aRunState.errorstr + " " + str(aRunState.getCurrent2RunSpeed())
                            aRunState.errors.append(self)
                            return True
                            pass
                        # abs(di * c - dk) < error with c in [c *(1-tol),c*(1+tol)]

                        # c = dk/di
        return False





class InChordKnNot(ErrorFeedBack):
    def __init__(self, *args, **kwargs):
        ErrorFeedBack.__init__(self, *args, **kwargs)
        self.errorstr=self.__class__.__name__
        self.costs = mykey([1])
        self.costs = mykey([0,1])

    def giveFeedback(self, output):
        ErrorFeedBack.giveFeedback(self, output)
        output.playTimingError(polite=True)
        self.feedbacktime=myglobals.gameState.getMidiTick()

    def check(self, aRunState):
        if not(aRunState is None or aRunState.lastRunState is None):
            if not (aRunState.knownChordInNoteMap is None or aRunState.lastRunState.knownChordInNoteMap is None):
                if aRunState.lastjumpRun == aRunState.lastRunState.lastjumpRun:

                    if aRunState.knownChordInNoteMap.innote is aRunState.lastRunState.knownChordInNoteMap.innote:
                        return False

                    if aRunState.getKnownChord is None or aRunState.getKnownChord is theUnknownChord :
                        return False

                    if aRunState.lastRunState.getKnownChord is None or aRunState.lastRunState.getKnownChord is theUnknownChord :
                        return False

                    #dk = abs(aRunState.getKnownChord().myoffset - aRunState.lastRunState.getKnownChord.myoffset)
                    #dk = abs(aRunState.getKnownNote().myoffset - aRunState.lastRunState.getKnownNote.myoffset)
                    di = abs(aRunState.knownChordInNoteMap.innote.myoffset - aRunState.lastRunState.knownChordInNoteMap.innote.myoffset)
                    firstchord = aRunState.getKnownChord()
                    secondchord =  aRunState.lastRunState.getKnownChord()

                    # bad dk is given and should not be aprox by ischordms
                    #if dk < ischordms:
                    #if aRunState.knownChordInNoteMap.knownChord.pos == aRunState.lastRunState.knownChord.pos:
                    if not(firstchord is secondchord):
                        if di * max(1,aRunState.rspeed(d=1))< ischordms:
                            self.derrorstr = "That is not a chord!\n" + "di * aRunState.rspeed(d=1)< ischordms\n" + " ".join(map(str,[di,aRunState.rspeed(d=1),ischordms]))
                            aRunState.errors.append(self)
                        else:
                            # Timming error
                            pass
                    # abs(di * c - dk) < error with c in [c *(1-tol),c*(1+tol)]

                    # c = dk/di



class RunSpeedChange(ErrorFeedBack):
    def __init__(self, *args, **kwargs):
        ErrorFeedBack.__init__(self, *args, **kwargs)
        self.errorstr=self.__class__.__name__
        self.costs = mykey([0,1])


    def giveFeedback(self, output):
        ErrorFeedBack.giveFeedback(self, output)
        output.playTimingError(polite=True)
        self.feedbacktime=myglobals.gameState.getMidiTick()

class RunChordErrorTooLate(ErrorFeedBack):
    def __init__(self, *args, **kwargs):
        ErrorFeedBack.__init__(self, *args, **kwargs)
        self.errorstr=self.__class__.__name__
        self.costs = mykey([0,1])


    def giveFeedback(self, output):

        ErrorFeedBack.giveFeedback(self, output)
        #output.playTimingError(polite=True)
        self.song = MySong()
        self.song.fromXml2file('./Sounds/' + self.__class__.__name__ +'.xml')

        output.playError(self.song.mystream, polite=True)
        # why again??
        #self.feedbacktime=myglobals.gameState.getMidiTick()
        
    def check(self, aRunState):
        curspeed = aRunState.getCurrent2RunSpeed()
        if curspeed:
            if aRunState.rspeed() - curspeed > aRunState.speedtol:
                aRunState.errors.append(self)
                self.derrorstr = "This pause is too big!\naRunState.rspeed() - curspeed > aRunState.speedtol"
                self.derrorstr = self.derrorstr + "\n" + str(aRunState.rspeed())+ " - " + str(curspeed) + " > " +str(aRunState.speedtol)
                return True
            else:
                pass
                #aRunState.errorstr = "run speedtol error"
            pass

class RunChordErrorTooEarly(ErrorFeedBack):
    def __init__(self, *args, **kwargs):
        ErrorFeedBack.__init__(self, *args, **kwargs)
        self.errorstr=self.__class__.__name__
        self.costs = mykey([0,1])


    def giveFeedback(self, output):
        self.song = MySong()
        self.song.fromXml2file('./Sounds/' + self.__class__.__name__ +'.xml')
        ErrorFeedBack.giveFeedback(self, output)
        #output.playTimingError(polite=True)
        output.playError(self.song.mystream, polite=True)
        #self.feedbacktime=myglobals.gameState.getMidiTick()

    def check(self, aRunState):
        curspeed = aRunState.getCurrent2RunSpeed()
        if curspeed:
            if curspeed - aRunState.rspeed() > aRunState.speedtol:
                aRunState.errors.append(self)
                self.derrorstr = "You are too fast here!\ncurspeed - aRunState.rspeed() > aRunState.speedtol"
                self.derrorstr = self.derrorstr + "\n" + str(curspeed)+ " - " + str(aRunState.rspeed())+ " > " +str(aRunState.speedtol)
                return True
            else:
                pass
                #aRunState.errorstr = "run speedtol error"
            pass



        
class ChordTimeShift(ErrorFeedBack):
    def __init__(self, *args, **kwargs):
        ErrorFeedBack.__init__(self, *args, **kwargs)
        self.errorstr=self.__class__.__name__
        self.costs = mykey([0,1])

    def giveFeedback(self, output):
        ErrorFeedBack.giveFeedback(self, output)
        output.playTimingError(polite=True)
        self.feedbacktime=myglobals.gameState.getMidiTick()


class RunTimeShift(ErrorFeedBack):
    def __init__(self, *args, **kwargs):
        ErrorFeedBack.__init__(self, *args, **kwargs)
        self.errorstr=self.__class__.__name__
        self.costs = mykey([0,1])


    def giveFeedback(self, output):
        ErrorFeedBack.giveFeedback(self, output)
        output.playTimingError(polite=True)
        self.feedbacktime=myglobals.gameState.getMidiTick()





class RunJump(ErrorFeedBack):
    def __init__(self, *args, **kwargs):
        ErrorFeedBack.__init__(self, *args, **kwargs)
        self.errorstr=self.__class__.__name__
        self.costs = mykey([1,1])
        #self.costs = mykey([0,0])

    def giveFeedback(self, output):
        ErrorFeedBack.giveFeedback(self, output)
        output.playMelodieError(polite=True)
        self.feedbacktime=myglobals.gameState.getMidiTick()

    def check(self, aRunState):
        if aRunState.lastRunState:
            if aRunState.getKnownChord() == aRunState.lastRunState.getKnownChord():
                return False

            if aRunState.lastRunState.getKnownChord() and aRunState.lastRunState.knownChordInNoteMap.chordfull() and aRunState.lastRunState.getKnownChord().nextChord == aRunState.getKnownChord():
                return False


            if aRunState.checkPauseRun() or not(hasattr(aRunState.getInNote(),"last")):
                #aRunState.errors.append(NewTry())
                return False

            aRunState.errorstr = "run jump error"
            aRunState.errors.append(self)

            return True



class Jump2UnKnown(ErrorFeedBack):
    def __init__(self, *args, **kwargs):
        ErrorFeedBack.__init__(self, *args, **kwargs)
        self.errorstr=self.__class__.__name__
        self.costs = mykey([1,1])
        #self.costs = mykey([0,0])

    def giveFeedback(self, output):
        ErrorFeedBack.giveFeedback(self, output)
        output.playMelodieError(polite=True)
        # polite is 500 ms silence
        #output.playMelodieError(polite=False)
        self.feedbacktime=myglobals.gameState.getMidiTick()

    def check(self, aRunState):
        if aRunState.lastRunState is None:
            # Start
            return False

        if NewTry().check(aRunState):
            return False

        if aRunState.getKnownChord() is theUnknownChord:
        #if aRunState.lastRunState:
            if aRunState.lastRunState.getKnownChord() or True:
                aRunState.errors.append(self)
                self.derrorstr="I dont know what you\nare playing right now: "
                # + aRunState.getKnownChordInNoteMap.innote.next.noteName()
                return True
        return False


# jump to next, so innotes is innotes.last
# jump back, gracefully => we have in and in.next (but see in another order)

class NewTry(ErrorFeedBack):
    def __init__(self, *args, **kwargs):
        ErrorFeedBack.__init__(self, *args, **kwargs)
        self.errorstr=self.__class__.__name__
        self.newtryPause = 3000
        self.costs = mykey([1,0])

    #TODO erase this New try doesnt play an error
    #def giveFeedback(self, output):
        #ErrorFeedBack.giveFeedback(self, output)
        #output.playMelodieError(polite=True)
        #self.feedbacktime=myglobals.gameState.getMidiTick()

    def check(self, aRunState, iatime=None):

        if aRunState.getKnownChord() is theUnknownChord:
            if iatime:
                atime =iatime
            else:
                #atime = myglobals.gameState.myMidiController.getMidiTick()
                try:
                    atime = aRunState.getInNote().last.myoffset
                    atime = aRunState.getInNote().next.myoffset
                except:
                    return False
                    # start force gracefully
                    atime = - self.newtryPause



                    #atime = aRunState.getInNote().myoffset
                    #atime = aRunState.getInNote().next.myoffset
                    #print aRunState.getInNote().__dict__



            #logger.debug("checkPauseRun " + str(aRunState))

            """ something went wrong, no expected time..
            expectedtime= None
            if aRunState.lastRunState:
                #expectedtime = aRunState.lastRunState.nextKnownNoteDeltaTime()
                expectedtime = aRunState.nextKnownNoteDeltaTime()


            #expectedtime = aRunState.nextKnownNoteDeltaTime()
            if expectedtime is None:
                logger.debug("eos")

            """
            expectedtime=0
            logger.debug(" check : " + str(expectedtime + self.newtryPause) +" < " + str(atime - aRunState.getKnownChordInNoteMap().innote.myoffset ))
            logger.debug(str(atime) + " < " +str(aRunState.getKnownChordInNoteMap().innote.myoffset) )

            #if expectedtime + self.appendPause < abs(atime - aRunState.getKnownChordInNoteMap().innote.myoffset):
            if expectedtime + self.newtryPause < abs(atime - aRunState.getKnownChordInNoteMap().innote.myoffset):
                # newtry
                logger.debug("NewTry")
                self.derrorstr="a long Pause"
                aRunState.errors.append(self)
                return True


        return False








