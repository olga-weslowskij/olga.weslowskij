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
import code

import logging
from Game.myKey import mykey
from Game.myKnownChord import theUnknownChord
from Game.myJumpChordsAndSpeedTols import MyJumpChordsAndSpeedTols
from Game.myLevenshteinChallenge import MyLevenshteinChallenge
from Game.myMelodyRating import KnChordInTimeTooLate
from Game.myMelodyRun import RunState
from Game.mySong import MySong
from Game.myStream import MyStreamNoteItemFutureProxy, MyStream
from mylibs.priorityQueue import PriorityQueue

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
#logger.setLevel(logging.INFO)
#logger.setLevel(logging.DEBUG)
logger.setLevel(logging.NOTSET)


class MyRunStateChallenge(MyLevenshteinChallenge):
    def __init__(self):
        super(MyRunStateChallenge, self).__init__()
        self.speed = None
        self.create_edge_fly = self.create_edge_all
        self.jumpToStates = MyJumpChordsAndSpeedTols()

        self.bestRunOnIn=PriorityQueue(key=lambda n: (n.mystream,n.pos), maxitems=20)

        #self.bestRunOnIn[self.innotes[-1]]=PriorityQueue(key=lambda x: (x.rcost[0:2],-x.lenlist), maxitems=1)

        self._paused = True

        self.name = None

    def bestActiveAbs(self):
        return self.bestActive()

    def checkPaused(self, atime):
        """
        for x in self.noNextInNoteMappings.values():
            try:
                if x.checkPauseRun(iatime=atime) is False:
                    self._paused = False
                    return False
            except:
                pass
        self._paused = True

        return True
        """
        longestexpected = self.noNextInNoteMappings.getLongestTime()

        if longestexpected:
            if longestexpected.checkPauseRun(iatime=atime) is False:
                self._paused = False
                return False
        return True




    @property
    def paused(self):
        return self._paused

    def setStartSelection(self, stream, speed, aspeedtol):
        # appending prestart notes

        self.jumpToStates.chordMap={}
        self.jumpToStates.notesdict={}

        for x in stream:
            self.jumpToStates.registerNote(x , speed, aspeedtol)

        self.challengestartnote=stream[-1]


    def errorcut(self,r):
        m = r
        v = m.getKnownChordInNoteMap()

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug( str(self.name) + " " + " errorcut for: " + r.prettyprint() +"\nError" + str(self.seen[r]) + " maxerror " + str(self.maxerror) + " runerror "+ str(None) )
        # global jumps
        if self.maxerror is not None:
            #if self.seen[r]- r.rcost > self.maxerror:
            #if self.seen[r] > self.maxerror:
            if self.seen[r][0:2] > self.maxerrorAtKnownnote.get(v.knownChord, self.maxerror)[0:2]:

                # just save Notes between start and endnote
                #if v.knownote.pos >= self.challengestartnote.pos:

                #self.cut[r]=r

                logger.debug(str(self.name) + " " + "..cutted")
                return True

        """
        # run cutts
        if r.lastjumpRun and True:
            #logger.debug(str(self.name) + " " + "has lastjumpRun ")
            if rbest is not None:
                #logger.debug(str(self.name) + " " + "has rbest ")

                if self.seen[r][0:2] > rbest[0:2]:
                # cut on error
                #if self.seen[r][0:1] > self.seen[r.lastjumpRun][0:1]:

                    #self.cut[r]=r
                    #self.create_jump_back(aprerun=r)
                    logger.debug(str(self.name) + " " + "..run cutted")
                    return True


        if r.lastjumpRun:
            #logger.debug(str(self.name) + " " + "has lastjumpRun ")
            # cut on error and jump
            if rbest is not None or True:
                # 4 > None in python
                #logger.debug(str(self.name) + " " + str(self.seen[r][0:1]) +  " > "+ str(self.seen[r.lastjumpRun][0:1]))
                if self.seen[r][0:1] > self.seen[r.lastjumpRun][0:1]:
                    #self.cut[r]=r
                    self.create_jump_back_edge(aprerun=r)
                    logger.debug(str(self.name) + " .. cutted on error" )
                    return True


        """

        logger.debug(str(self.name) + " " + "not cutted")
        return False



    def target_reached(self, r):

        try:
            # log best
            self.bestRunOnIn[r.getInNote()].add(r)
        except Exception as e:
            print(e)
            code.interact(local=locals())


        #b = (v.innote.__repr__()) == self.target.__repr__()
        #b = v.innote is self.target
        m = r
        v = m.getKnownChordInNoteMap()
        if logger.isEnabledFor(logging.INFO) and r.lenlist > 1:
            logger.info(str(self.name) + " " + "checking targets for " + r.prettyprint())
            logger.info(str(self.name) + " " + "targets " + str(self.targets))
            #logger.info(str(self.name) + " " + "Mr id " + str(id(r)))

        
        #logger.debug(str(self.name) + " and targets" + str(self.targets))

        for tchord in self.targets:
            if logger.isEnabledFor(logging.INFO):
                #pass
                logger.info(str(self.name) + " " + "check " + tchord.prettyprint() +" vs " + v.knownChord.prettyprint())
                logger.info(str(self.name) + " " + " v.knownChord == tchord : " + str(v.knownChord == tchord))
                logger.info(str(self.name) + " " + "v.chordfull(): " + str(v.chordfull()))
                #code.interact(local=locals())

            if (v.knownChord == tchord and v.chordfull()):
                #logger.info("target "+ str((tnote,tchord)) + "reached " + str( self.seen[r]- r.rcost) + " errors")

                a = self.donelist.get(tchord,[])
                a.append(r)
                self.donelist[tchord]=a

                if self.retondone == tchord:
                    logger.info(str(self.name) + " " + "target reached: ret and done")
                    return True
                logger.info(str(self.name) + " " + "target reached")

        return False

    """
    def target_reached(self, r):
        return MyLevenshteinChallenge.target_reached(self,r)
    """


    def bestActive(self):
        try:
            ain =self.innotes[-1]
        except:
            #that is messy
            return self.bestRunOnIn.peek()
        return self.bestRunOnIn[ain].peek(d=None)

        """
        if len(self.noNextInNoteMappings.keys())>0:
            return min(self.noNextInNoteMappings.keys(), key = lambda a: (self.seen[a][0],self.seen[a][1], -a.lenlist))
        return None
        """

    def updatePause(self, aTime):
        findnewbest = False

        for x in self.noNextInNoteMappings.values():
            y = self.bestRunOnIn[x.getInNote()].peek()
            if y is x:
                oldcosts = y.rcost
                if KnChordInTimeTooLate().check(x, aTime):
                    x.updatercost()
                    if y.rcost > oldcosts:
                        # need to update best
                        # update doesnt work cause key is changed
                        #self.bestRunOnIn[x.getInNote()].update(x)
                        # update / delete that item
                        # pop smallest only works cause we assuming size 1 tree
                        self.bestRunOnIn[x.getInNote()].pop_smallest()

                        findnewbest = True
            else:
                if KnChordInTimeTooLate().check(x, aTime):
                    x.updatercost()


        if findnewbest:
            #print "FINDING NEW BEST DUE Best was a chord and not played so error due time"
            #y = self.bestRunOnIn[x.getInNote()].peek()
            #print "before",  y.prettyprint()
            for x in self.noNextInNoteMappings.values():
                self.bestRunOnIn[x.getInNote()].add(x)
                #y = self.bestRunOnIn[x.getInNote()].peek()
                #print x.prettyprint()
                #if y.rcost > x.rcost:
                    # this should never happen
                    #1/0


            #y = self.bestRunOnIn[x.getInNote()].peek()
            #print "after ", y.prettyprint()






    def update(self):
        # poor mans init
        if self.name is None:
            self.name = "RunState"
            #self.create_idontknowwhereyouare(self.innotes[-1])
            self.create_idontknowwhereyouare(ain=self.innotes[-1])

        super(MyLevenshteinChallenge, self).update()
        if not hasattr(self,"newnote"):
            self.newnote = False

        activebest=self.bestActive()
        if logger.isEnabledFor(logging.INFO):
            if activebest:
                abrepr =str(activebest.prettyprint())
                #abrepr =str(activebest)
            else:
                abrepr = "None"
                #code.interact(local=locals())

        if self.newnote and logger.isEnabledFor(logging.DEBUG):
            self.newnote = False
            logger.info( str(self.name) + " all noNextInNoteMappings " + self.innotes[-1].prettyprint())
            for x in self.noNextInNoteMappings.keys():
                logger.info( str(self.name) + x.prettyprint())
                logger.info(str(self.name) + " error "+ str(self.seen[x]))
    
    def add_stream(self, s):
        for x in s:
            self.add_note(x)
    
    
    def add_note(self, aNote):
        logger.debug(str(self.name) + " " + "add_note " + str(aNote))
        """
        if hasattr(aNote,"last"):
            self.create_where_are_you(aNote.last)
        """
        self.innotes.append(aNote)
        self.bestRunOnIn[self.innotes[-1]]=PriorityQueue(key=lambda x: (x.rcost[0:2],-x.lenlist), maxitems=1)
        #self.bestRunOnIn[self.innotes[-1]]=PriorityQueue(key=lambda x: (x.costs()[0:2],-x.lenlist), maxitems=1)
        self.newnote = True

    def create_edge_fly(self, v):
        self.create_edge_all(v)

    def myadd_node(self,anode):
        anode.updateAll()
        self.G.add_node(anode)
        anode.rcost = anode.rcost + anode.costs()
        self.pos[anode] = anode.knownChordInNoteMap.drawpos(self.drawposdict)
        return anode

    def create_edge_all(self, ir):
        #logger.debug(str(self.name) + " " + "create_edge_all " + str(r.__dict__))
        #logger.debug(str(self.name) + " " + "create_edge_all " + str(r))
        #logger.debug( str(self.name) + " " + "create_edge_all " + str(id(r)))
        #logger.debug(str(self.name) + " " + "id " + str(id(r)))
        
        #r = RunState()
        r = ir

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(str(self.name) + " error "+ str(self.seen[r]) + " flying "+ r.prettyprint())

        m = r

        #print "edges before fly", self.G.edges()

        #m = MelodyRating()

        v = r.getKnownChordInNoteMap()
        In = v.innote
        Kn = v.knownChord

        Knnext = v.activeKnownChord()

        Innext = None

        if hasattr(In, "next"):
            Innext = In.next
        #logger.debug(str(self.name) + " Knnext " + str(Knnext))
        #Knnext = v.nextKnownChordNote()

        #if hasattr(Kn, "next"):

        addededges=0



        #logger.debug(str(self.name) + " len(Kn.getChordtonesofType(Innext))" + str(len(Kn.getChordtonesofType(In.next))))
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(str(self.name) + " id(v) " + str(id(v)))
            logger.debug(str(self.name) + " In " + str(In))
            if hasattr(In, "next"):
                logger.debug(str(self.name) + " Innext " + str(Innext))
            if Kn:
                logger.debug(str(self.name) + " Kn " + str(Kn))
                logger.debug(str(self.name) + " Kn " + str(Kn.prettyprint()))

        #logger.debug(str(self.name) + " playedchords " + " id " + str(id(v.playedChordNotes)) + " " + str(v.playedChordNotes))



        # where are you and "skip"

        #if Kn is None and hasattr(In, "next") and True:
        if Kn is theUnknownChord and Innext and True:
            # jump
            #self.create_jump_edges(aprerun=r)
            logger.debug( str(self.name) + " jumping " + str(id(r)))
            addededges=addededges + self.create_jump_edges(aprerun=r)
            #self.create_jump_edges(aprerun=None)


        #if not hasattr(In, "next"):
        #if not hasattr(In, "next") or In is None:
        if Innext is None:
            logger.debug( str(self.name) + " adding noNextInoteMappings " + str(id(r)))
            self.noNextInNoteMappings.add(r)
            addededges=addededges+1

        # forward
        #if hasattr(In, "next"):
        if Innext:
        #print "flying ", v
            #if self.nodefullexpandedAll.get(o, 0) < 2 or True:
            #if self.nodefullexpandedAll.get(o, 0) < 2:
            if True:
                #print "flying  cache ", v
                #self.nodefullexpandedAll[o]= 2
                #v.expanded[Innext] = False

                # transpose

                #add_edge(i,i+1,Intervall=aMap)

                # in chord
                if Kn:
                    if not v.chordfull():
                        for x in Kn.getChordtonesofType(Innext):
                            #print "in Chord Transpose"
                            # check if played already
                            skip = False
                            for note in v.playedChordNotesgood:
                                if note is x:
                                    skip = True
                                    #logger.debug("x is already used")
                                    #logger.debug(str(x))
                                    #logger.debug(str(v.playedChordNotes))
                                    #logger.debug(str(note))
                            if not skip:
                                rnew= r.extend()
                                rnew.knownChordInNoteMap =  self.createKnownChordPos(Innext,x.chord,v)
                                rnew = self.myadd_node(rnew)

                                logger.debug( str(self.name) + " adding " + str(id(rnew)) + " " + rnew.errorstr)
                                self.add_edge(r,rnew,str="in Chord",weight=rnew.costs())
                                addededges=addededges+1



                    if v.chordfull():
                        logger.debug( str(self.name) + " v.chordfull() " + str(v.chordfull()))
                        if not v.activeKnownChord() is None:
                            logger.debug( str(self.name) + " v.nextKnownChord() " + str(v.activeKnownChord()))
                            logger.debug( str(self.name) + " v.nextKnownChord().getChordtonesofType(Innext) " + str(v.activeKnownChord().getChordtonesofType(Innext)))
                            for x in v.activeKnownChord().getChordtonesofType(Innext):
                                #print "out Chord Transpose"
                                rnew = r.extend()
                                rnew.knownChordInNoteMap = self.createKnownChordPos(Innext, x.chord, None)

                                #rnew.updateRunSpeed()

                                rnew.errorstr="out Chord"

                                rnew = self.myadd_node(rnew)

                                #self.add_edge(v,tmp,str="Transpose out Chord Timming Good "+ str([rmid, tmpr.getCurrent2RunSpeed()]), weight=0)

                                logger.debug( str(self.name) + " adding " + str(id(rnew)) + " " + rnew.errorstr)
                                #self.pushNode(rnew, self.seen[r])

                                self.add_edge(r, rnew, str="out Chord" + str([str(r.getCurrent2RunSpeed())[0:5], str(rnew.getCurrent2RunSpeed())[0:5]]), weight=rnew.costs())
                                addededges=addededges+1

                                #return

        return addededges


    def create_idontknowwhereyouare(self, aIn=None, push =True, costs=None):
        #for anote in self.challengestartnote.
        # update and add_note synchron ..
        if aIn is None:
            In = MyStreamNoteItemFutureProxy(self.innotes,0)
            #In = self.innotes[-1]
        else:
            In = aIn

        ntmp = self.createKnownChordPos(In, theUnknownChord, None)

        r = RunState()
        r.knownChordInNoteMap = ntmp
        r.lastRunState = None

        r.errorstr="Start"

        if self.speed:
            r.speed = self.speed

        #if self.speedtol is None:
        #if self.speedtol == 0.0:
        # BUG: speedtol for Olga is frozen cause olga has only one idontknowwhereareyou state
        # fixed: speedtol is set on jump
        #if r.speedtol is None:
        #    r.speedtol = self.speedtol

        if costs is None:
            r.rcost = mykey([0, 0 ,-1])
        else:
            r.rcost = costs

        self.myadd_node(r)

        if push:
            self.pushNode(r, r.rcost)

        return r



    def create_jump_edges(self, aIn=None, aprerun=None):
        #for anote in self.challengestartnote.

        # update and add_note synchron ..

        #In = self.innotes[-1]

        prerun = aprerun

        if aIn:
            In=aIn

        if aprerun:
            prerun=aprerun
            m = prerun
            v = m.getKnownChordInNoteMap()
            if v.innote:
                Ino = v.innote
                if logger.isEnabledFor(logging.INFO):
                    logger.info(str(self.name) + " jumping aprerun " + aprerun.prettyprint())
                #logger.debug(str(self.name) + " jumping aprerun has In: " +str(Ino))
            else:
                Ino = self.innotes[-1]


            lennewnodes=0
            if hasattr(Ino, "next"):
                In = Ino.next
                lennewnodes = len(self.jumpToStates.getChords(In))
                logger.debug(str(self.name) + " jumping to all : " +str(In)+ " notes #:"  + str(lennewnodes ))

        #logger.debug(str(self.name) + " HALLO!!! " +str(len(self.jumpToStates.getChords(In)))+ " notes")


        for (tmp, speed, speedtol) in self.jumpToStates.getChords(In):

            #for tmp in self.challengestartnote.chord.notes:

                #ntm8p = self.createNoteMap(In, tmp, None, justnew=True)


                if aprerun:
                    ntmp = self.createKnownChordPos(In, tmp, v)

                startcost = 0

                if prerun:
                    oldntmp=prerun.getKnownChordInNoteMap()

                if ntmp is not None:
                    m= None

                    if prerun:
                        rnew = prerun.extend()
                    else:
                        rnew = RunState()

                    rnew.speedtol = speedtol
                    rnew.speed = speed
                    
                    rnew.knownChordInNoteMap = ntmp

                    rnew.firstRunMelodyRating=None



                    #code.interact(local=locals())

                    """
                    if self.checkNewTry(r, In.myoffset):
                        m=NewTry(oldntmp, ntmp)
                        m.errorstr="New Try"

                    else:
                        m=RunJump(oldntmp, ntmp)
                        m.errorstr="jump"
                    """

                    #m.getCurrent2RunSpeed()=None

                    rnew.errorstr="jump"

                    #rnew.errors.append(RunJump())
                    rnew.lastjumpRun = rnew





                    #code.interact(local=locals())

                    #self.add_edge(prerun, rnew, str="jump", weight = mykey([1, 1]))

                    # in is free out cost [1,1]

                    self.myadd_node(rnew)

                    if logger.isEnabledFor(logging.DEBUG):
                        logger.info(str(self.name) + " adding " + rnew.prettyprint())
                    self.add_edge(prerun, rnew, str="jump in", weight = rnew.costs())
                    #self.add_edge(prerun, rnew, str="jump in", weight = mykey([0,0]))
                    #logger.debug(str(self.name) + " adding " + m.errorstr +" " + str(rnew.rcost))


                    #logger.debug(str(self.name) + " adding " + str(id(rnew)) +" " + m.errorstr)


                    #logger.debug(str(self.name) + " pushing " + rnew.prettyprint())

        return lennewnodes
    


if __name__ == '__main__':

    for case in xrange(15):
        c = MyRunStateChallenge()

        if True:
            if case == 0:
                song=MySong()
                #self.song.fromXml2file("Output.xml")

                song.fromXml2file("./Songs/OlgaXml/Juravlev.xml")

               # song.mystream.song = song
                #song.mystream=song.mystream.decorate()

                c.jumpToStates.registerStream(song.mystream, 0.25)

                print "go"
                c.update()
                oa=None


                start = len(song.mystream) -20
                #start = 0
                end = len(song.mystream)
                for i in xrange(start,end):
                    x = song.mystream[i]
                    """

                for x in song.mystream:
                    """

                    nn = x.note.clone()
                    nn.myoffset = nn.myoffset * 0.750
                    c.add_note(nn)
                    c.update()

                    if c.bestActive() is None:
                        #print str(x)
                        break
                    else:
                        #print str(x)
                        oa = c.bestActive()

                print "Done"
                print oa.prettyprint(history=True)
                #print c.bestActive().prettyprint(history=True)

                #pdb.set_trace()




            if case == 0:
                song=MySong()
                #self.song.fromXml2file("Output.xml")

                song.fromXml2file("./Songs/OlgaXml/Juravlev.xml")

               # song.mystream.song = song
                #song.mystream=song.mystream.decorate()

                c.jumpToStates.registerStream(song.mystream, 0.25)

                print "go"
                c.update()
                oa=None


                start = len(song.mystream) -20
                #start = 0
                end = len(song.mystream)
                for i in xrange(start,end):
                    x = song.mystream[i]
                    """

                for x in song.mystream:
                    """

                    nn = x.note.clone()
                    nn.myoffset = nn.myoffset * 0.750
                    c.add_note(nn)
                    c.update()

                    if c.bestActive() is None:
                        #print str(x)
                        break
                    else:
                        #print str(x)
                        oa = c.bestActive()

                print "Done"
                print oa.prettyprint(history=True)
                #print c.bestActive().prettyprint(history=True)

                #pdb.set_trace()

        try:

            if case == 10:
                song=MySong()
                song.fromXml2file("./tests/Output.xml")

                s = MyStream()
                s.fromXml2file("./tests/olga_no_edges_kn.xml")

                s.song = song
                song.mystream=s

                c.jumpToStates.registerStream(s)




                si = MyStream()


                si.fromXml2file("./tests/olga_no_edges_in.xml")
                si.shift(0 - si[0].myoffset)
                c.add_stream(si)





            if case == 1:
                song=MySong()
                song.fromXml2file("./tests/Output.xml")

                c.jumpToStates.registerStream(song.mystream.decorate())
                #myglobals.OlgaMode.challenge.speedtol=0.0

                s = MyStream()
                s.fromXml2file("./tests/i.xml")
                c.add_stream(s)



            if case == 3:
                song=MySong()
                song.fromXml2file("./tests/Output.xml")



                s = MyStream()

                end = len(song.mystream)
                start = 0

                start = 3
                end = 20

                for x in range(start,end):
                    n = song.mystream[x]
                    s.append(n)

                s = s.decorate()
                s.song = song
                song.mystream=s
                c.jumpToStates.registerStream(s)
                #myglobals.OlgaMode.challenge.speedtol=0.0


                s = MyStream()


                s.fromXml2file("./tests/i2s.xml")
                s.shift(0 - s[0].myoffset)
                c.add_stream(s)


            # worst case
            if case == 2:
                song=MySong()

                #song.fromXml2file("./tests/Output.xml")

                so = MyStream()
                so.fromXml2file("./tests/midi40.xml")

                song.mystream=so.decorate()
                song.mystream.song = song


                c.jumpToStates.registerStream(song.mystream, 0.25)
                #myglobals.OlgaMode.challenge.speedtol = 0.0


                s = MyStream()
                s.fromXml2file("./tests/midi60.xml")
                c.add_stream(s)

            if case == 5:
                song=MySong()

                #song.fromXml2file("./tests/Output.xml")

                so = MyStream()
                so.fromXml2file("./tests/jump_error_known60.xml")

                song.mystream=so
                so.song= song


                c.jumpToStates.registerStream(so)

                #myglobals.OlgaMode.challenge.speedtol=0.0


                s = MyStream()
                s.fromXml2file("./tests/jump_error_played60.xml")
                c.add_stream(s)


            if case == 6:
                song=MySong()

                #song.fromXml2file("./tests/Output.xml")

                so = MyStream()
                so.fromXml2file("./tests/test_kn_miss.xml")

                song.mystream=so
                so.song= song


                c.jumpToStates.registerStream(so)

                #myglobals.OlgaMode.challenge.speedtol=0.0


                s = MyStream()
                s.fromXml2file("./tests/test_in_miss.xml")
                c.add_stream(s)


                print "case " + str(case)

                print c.bestActive().prettyprint(history=True)

        except Exception, e:
            print "case " + str(case) + " fails: " +str(e)

    
