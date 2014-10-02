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
import copy
import logging
from Game.myKey import mykey
from Game.myMelodyRating import RunJump, NewTry, InChordKnNot, Jump2UnKnown, KnChordInTimeTooLate, RunChordErrorTooEarly, RunChordErrorTooLate

from Game.myStream import MyStream, ischordms
from mylibs.myUniqueList import MyUniqueList

logger = logging.getLogger('mydeeprate')
hdlr = logging.FileHandler('./mydeeprate.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)


# 1 sec pause is considered a Pause
newtryPause = 1000

class RunState(object):
    def __init__(self):
        self.knownChordInNoteMap=None
        self.speed =None


        # was
        #self.speedtol= 0.0
        self.speedtol= None


        #self.errorstrs={}
        self.errors=MyUniqueList()
        #self.errors.key=lambda x: str(x)
        self.errors.key=lambda x: x.__class__.__name__

        # list includes self, so lenlist starts at 1
        self.lenlist=1


        self.lastTimmingUpdate=None



        # run
        self.minRightSpeedRunState=None
        self.maxRightSpeedRunState=None
        self.firstRunState=None

        # the previous
        self.lastRunState = None

        # previous specials
        self.currentTimingRun=None
        self.lastfullchordRun=None
        self.lastjumpRun = None

        self.rcost=mykey([0])


        #caches
        self._EqValueState=None
        self._list=None
        self.__2rspeed = None


        


    def checkPauseRun(self, iatime=None):
        if iatime:
            atime =iatime
        else:
            #atime = myglobals.gameState.myMidiController.getMidiTick()
            try:
                atime = self.getInNote().last.myoffset
            except:
                atime = self.getInNote().myoffset
                #print self.getInNote().__dict__


        logger.debug("checkPauseRun " + str(self))

        expectedtime = self.nextKnownNoteDeltaTime()
        if expectedtime is None:
            logger.debug("eos")
            expectedtime=0

        logger.debug(" check : " + str(expectedtime + newtryPause) +" < " + str(atime - self.getKnownChordInNoteMap().innote.myoffset ))
        logger.debug(str(atime) + " < " +str(self.getKnownChordInNoteMap().innote.myoffset) )

        if expectedtime + newtryPause < abs(atime - self.getKnownChordInNoteMap().innote.myoffset):
            # newtry
            logger.debug("NewTry")
            return True
        return False

        return None


    def checkJump(self):
        if self.lastRunState:
            if self.getKnownChord() == self.lastRunState.getKnownChord():
                return

            if self.lastRunState.getKnownChord() and self.lastRunState.knownChordInNoteMap.chordfull() and self.lastRunState.getKnownChord().nextChord == self.getKnownChord():
                return


            if self.checkPauseRun() or not(hasattr(self.getInNote(),"last")):
                self.errors.append(NewTry())
                return

            self.errorstr = "run jump error"
            self.errors.append(RunJump())


    # find errors
    def updateAll(self):
        #RunJump().check(self)
        Jump2UnKnown().check(self)
        #self.checkJump()
        self.updateRunSpeed()
        KnChordInTimeTooLate().check(self, self.getInNote().myoffset)
        InChordKnNot().check(self)
        #self.checkInChordTiming()
        #self.checkMelodyTiming()
        if self.speedtol:
            if RunChordErrorTooEarly().check(self) or RunChordErrorTooLate().check(self):
                # how to handle timingerrors in olga
                # new run
                self.maxRightSpeedRunState = None
                self.minRightSpeedRunState = None


        if self.lastRunState:
            if self.lastRunState.knownChordInNoteMap.chordfull():
                self.lastfullchordRun = self.lastRunState

        if self.knownChordInNoteMap.chordfull():
            self.lastfullchordRun = self

        self._list=None


    def updateRunSpeed(self):
        if self.firstRunState==None:
            self.firstRunState= self
            self.minRightSpeedRunState = self
            self.maxRightSpeedRunState = self

            self.currentTimingRun=self

        if self.minRightSpeedRunState is None:
            self.minRightSpeedRunState = self
        if self.maxRightSpeedRunState is None:
            self.maxRightSpeedRunState = self


        if self.getCurrent2RunSpeed():
            if self.minRightSpeedRunState.getCurrent2RunSpeed() is None:
                self.minRightSpeedRunState = self
            if self.maxRightSpeedRunState.getCurrent2RunSpeed() is None:
                self.maxRightSpeedRunState = self

            if self.minRightSpeedRunState.getCurrent2RunSpeed() > self.getCurrent2RunSpeed():
                self.minRightSpeedRunState = self
            if self.maxRightSpeedRunState.getCurrent2RunSpeed() < self.getCurrent2RunSpeed():
                self.maxRightSpeedRunState = self




    # == RightSpeed
    def getCurrent2RunSpeed(self, aprerun=None):
        if self.__2rspeed:
            return self.__2rspeed
        if aprerun is None:
            prerun = self.lastRunState
        else:
            prerun=aprerun

        try:
            #if self.lastjumpRun != prerun.lastRunState:
            #    return None
            #kn = self.getKnownChord()
            #dk = abs(self.getKnownChord().myoffset - prerun.getKnownChord().myoffset)
            dk = abs(self.getKnownNote().myoffset - prerun.getKnownNote().myoffset)

            # timimg based on lastRunState
            di =abs(prerun.getInNote().myoffset- self.getInNote().myoffset)
            #print str((dk * 1.0)/ di)

            # smoothing ??
            if dk < ischordms/4 or di < ischordms/4:
                return None

            self.__2rspeed = (dk * 1.0)/ di
            return self.__2rspeed

        except Exception, e:
            #print str(e)
            return None

    def getKnownChordInNoteMap(self):
        return self.knownChordInNoteMap


    def getKnownChord(self):
        return self.knownChordInNoteMap.knownChord

    
    def getKnownNote(self):
        return self.knownChordInNoteMap.knownnote

    
    def getInNote(self):
        return self.knownChordInNoteMap.innote


    def getKnownStream(self):
        ret = MyStream()
        for x in self.list:
            ret.append(x.getKnownNote())
        return ret

    def getInStream(self):
        ret = MyStream()
        for x in self.list:
            ret.append(x.getInNote())
        return ret
    



    @property
    def errorstr(self):
        ret = ""
        ret = ret.join(map(str, self.errors))
        return ret

    # ignored
    @errorstr.setter
    def errorstr(self,value):
        pass

    # this seems more extendRun rename?
    def extend(self):
        ret = copy.copy(self)        
        ret.lastRunState = self
        ret.lenlist = self.lenlist+1

        ret.errors=MyUniqueList()
        #ret.errors.key=lambda x: str(x)
        ret.errors.key=str
        #ret.errors = []

        ret.__2rspeed=None
        ret._EqValueState=None
        return ret    


    def prettyprint(self, history=False):
        #txt = "id: " + str(id(self)) + " MR id " + str(id(self)) + " " + " MR id " + str(id(self.currentTimingRun))+" "
        
        if history:
            l=self.list
        else:
            l = [self]
        txt = "id: " + str(id(self)) +" "
        for x in l:
            #kn = x.getKnownNote()
            kn = x.getKnownNote()
            if kn:
                knp = kn.prettyprint()
                kno = kn.myoffset
            else:
                knp = "RealNone"
                kno = ""

            ain = x.getInNote()
            try:
                inp = ain.prettyprint()
                ino = ain.myoffset
            except:
                inp = "None"
                ino = ""

            #txt = txt  + str(inp) + " -> " + str(knp)+ " at ("+ str(kno) +" "+ str(ino)+ "): " + x.errorstr + ", "
            #txt = txt  + str(inp) + " -> " + str(knp)+ ": " + x.errorstr + " rr: "+ str(x.getCurrent2RunSpeed()) + " r: " + str(x.rspeed(d=None))+  " rc: "+ str(x.rcost)+ " len(x.errors) " + str(len(x.errors))# + "\n"
            #self.updatercost()
            txt = txt  + x.knownChordInNoteMap.prettyprint() + ": " + x.errorstr + " rr: "+ str(x.getCurrent2RunSpeed()) + " r: " + str(x.rspeed(d=None))+  " rc: "+ str(x.rcost)+ " len(x.errors) " + str(len(x.errors))# + "\n"
            #txt = txt  + x.knownChordInNoteMap.prettyprint() + ": " + x.errorstr + " rr: "+ str(x.getCurrent2RunSpeed()) + " r: " + str(x.rspeed(d=None))+  " rc: "+ str(x.costs())+ " len(x.errors) " + str(len(x.errors))# + "\n"
            if history:
                txt = txt +"\n"
            if len(x.errors) > 0:
                pass
                #print x.errorstr
                #print self.errorstr
                #print "Done"

                #code.interact(local=locals())
            #", "

        return txt



    #def append(self, self, aprerun =None):
    

    # costs of this Event
    def costs(self):
        try:
            ret = mykey([0])
            for x in self.errors:
                ret = ret +  x.costs
            return ret
        except:
            #print ret
            #print x.errorstr
            #print x.costs
            pass


    def rspeed(self, d=None):
        if not (self.speed is None):
            return self.speed

        if self.minRightSpeedRunState and self.maxRightSpeedRunState:
            if self.minRightSpeedRunState.getCurrent2RunSpeed() and self.maxRightSpeedRunState.getCurrent2RunSpeed():
                return abs(self.minRightSpeedRunState.getCurrent2RunSpeed() +self.maxRightSpeedRunState.getCurrent2RunSpeed()) /2
        else:
            return d
        return d


    def updatercost(self):
        if self.lastRunState:
            self.rcost = self.lastRunState.rcost + self.costs()
        else:
            self.rcost = self.costs()



    def nextKnownNoteDeltaTime(self):
        try:
            tmp = self.knownChordInNoteMap.knownChord.nextChord.myoffset-self.knownChordInNoteMap.knownChord.myoffset
        except:
            tmp = None
        return tmp

    def nextKnownChordFirstNote(self):
        try:
            tmp = self.knownChordInNoteMap.knownChord.nextChord.notes[0]
        except:
            tmp = None
        return tmp


    def nextKnownNoteDeltaTimeLastGood(self):
        try:
            tmp = self.knownChordInNoteMap.knownChord.nextChord.myoffset-self.currentTimingRun.knownChordInNoteMap.knownChord.myoffset
        except:
            tmp = None
        return tmp


    def EqValueState(self):
        #if self._EqValueState is None or True:
        if self._EqValueState is None:
            if self.currentTimingRun is None:
                dstr = None
            else:
                dstr = repr(self.currentTimingRun.knownChordInNoteMap)
            #dstr = repr(self.currentTimingRun)
            #rstr=[repr(self.getKnownChordInNoteMap()), self.errorstr]

            rstr=repr(self.knownChordInNoteMap)
            #rstr = repr(self)

            #if self.rspeed() == 0.0:
            if self.speedtol is None:
            #if self.speedtol == 0.0:
                # no self.speedtol and speed
                #self._EqValueState = str(rstr)
                self._EqValueState = str([dstr, rstr])

            else:
                # speedtol and speed
                self._EqValueState = str([dstr, rstr ,str(self.rspeed()),self.speedtol])
        return self._EqValueState


    def EqState(self):
        return self.EqValueState()
        #return str([repr(self.currentTimingRun.getKnownChordInNoteMap()), repr(self.getKnownChordInNoteMap()), repr(self.minRightSpeedRunState), repr(self.maxRightSpeedRunState)])


    def __repr__(self):
        if self.currentTimingRun is None:
            dstr = None
        else:
            dstr = repr(self.currentTimingRun.knownChordInNoteMap)
        #dstr = repr(self.currentTimingRun)
        #rstr=[repr(self.getKnownChordInNoteMap()), self.errorstr]

        rstr=repr(self.knownChordInNoteMap)
        #rstr = repr(self)

        #if self.rspeed() == 0.0:
        if self.speedtol is None:
        #if self.speedtol == 0.0:
            # no self.speedtol and speed
            #return str(rstr)
            return str([dstr, rstr])
        else:
            # speedtol and speed
            return str([dstr, rstr ,str(self.rspeed()), self.speedtol])

    def __str__(self):
        return self.prettyprint()
        #return str([self.firstRunState, self.rspeed()])
        #return str([self.currentTimingRun, self.rspeed()])


    def __hash__(self):
        return hash((self.EqValueState()))

    def __cmp__(self, other):
        if other:
            try:
                return cmp(self.EqValueState(), other.EqValueState())
            except:
                return 1
        else:
            return -1

    @property
    def list(self):
        if self._list:
            return self._list

        self._list = []
        prerun = self
        while prerun:
            self._list.append(prerun)
            prerun = prerun.lastRunState

        self._list  = list(reversed(self._list))

        self.lenlist= len(self._list)

        return self._list
        #if self._list:
            #return self._list

