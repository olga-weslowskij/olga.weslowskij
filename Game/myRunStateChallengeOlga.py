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
from Game.myLevenshteinChallenge import MyLevenshteinChallenge
from Game.myMelodyRating import Wrong
from Game.myNote import theUnknownNote
from Game.myRunStateChallenge import MyRunStateChallenge
from mylibs.priorityQueue import PriorityQueue

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
#logger.setLevel(logging.INFO)
#logger.setLevel(logging.DEBUG)
logger.setLevel(logging.NOTSET)

class MyRunStateChallengeOlga(MyRunStateChallenge):
    def __init__(self):
        super(MyRunStateChallengeOlga, self).__init__()
        self.maxerror=None
        #self.bestRunOnIn=PriorityQueue(key=lambda x: x.rcosts[0:2])
        #self.bestRunOnIn=PriorityQueue(key=lambda n: (n, self.innotes[n].mystream), maxitems=10)
        self.bestRunOnIn=PriorityQueue(key=lambda n: (n.mystream,n.pos), maxitems=10)

        # do we need inevent now?
        # innotes hasent FutureProxy

        # psssh, dont tell anyone
        # MyStreamNoteItemFutureProxy is "StartEvent"
        #self.innotes.notes.append(MyStreamNoteItemFutureProxy(self.innotes,1))

        self.innotes.append(theUnknownNote)
        # rcosts is bad cause time can change errors (KnChordInNoteTooLate)
        self.bestRunOnIn[self.innotes[-1]]=PriorityQueue(key=lambda x: x.rcost[0:2], maxitems=1)

        # bad x.costs() is dynamic so our tree can get coruppted
        # wrong costs are current event costs only
        #self.bestRunOnIn[self.innotes[-1]]=PriorityQueue(key=lambda x: x.costs()[0:2], maxitems=1)

        self.newnote = None
        self.myinit()


    @property
    def bestabsrun(self):
        try:
            ain =self.innotes[-1]
        except:
            #that is messy
            return self.bestRunOnIn.peek()
        return self.bestRunOnIn[ain].peek(d=None)

    def bestActive(self):
        return self.bestRunOnIn[self.innotes[-1]].peek(d=None)



    def target_reached(self, r):
        self.bestRunOnIn[r.getInNote()].add(r)
        return super(MyRunStateChallengeOlga,self).target_reached(r)

    def errorcut(self,r):
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(str(self.name) + " " + "errorcut for " + r.prettyprint())

        try:
            """
            # >= is consuming notes AB|CDEFAB -> ABCDEF
            # jumps in ab, KnChordInnot AB Wrong
            """
            inb= self.bestRunOnIn[r.getInNote()].peek(d=False)
            if inb and not (r.getKnownChord() is theUnknownChord):
                if r.rcost > inb.rcost + mykey([1,1]):
                    if logger.isEnabledFor(logging.DEBUG):
                        logger.debug(str(self.name) + " cutted True")
                    return True

            ret = super(MyRunStateChallengeOlga,self).errorcut(r)
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(str(self.name) + " cutted " +str(ret))
            return ret
        except:
            code.interact(local=locals())

    def myinit(self):
        if self.name != "RunStateOlga":
            self.name = "RunStateOlga"
            #pdb.set_trace()
            super(MyRunStateChallengeOlga,self).create_idontknowwhereyouare(aIn=self.innotes[-1])



    def update(self):
        if logger.isEnabledFor(logging.INFO):
            if self.bestabsrun:
                abrepr =str(self.bestabsrun.prettyprint())
                logger.info( str(self.name) + " update pre bestabsrun" + abrepr)
                #abrepr =str(activebest)
            else:
                abrepr = "None"
                #code.interact(local=locals())

        #
        super(MyLevenshteinChallenge, self).update()
        #super(MyRunStateChallengeOlga, self).update()


        if logger.isEnabledFor(logging.INFO):
            if self.bestabsrun:
                abrepr =str(self.bestabsrun.prettyprint(history=True))
                logger.info( str(self.name) + " update past bestabsrun" + abrepr)
                #abrepr =str(activebest)
            else:
                abrepr = "None"


        if self.newnote and logger.isEnabledFor(logging.DEBUG):
            self.newnote = False
            logger.info( str(self.name) + " all noNextInNoteMappings " + self.innotes[-1].prettyprint())
            for x in self.noNextInNoteMappings.keys():
                logger.info( str(self.name) + x.prettyprint())
                logger.info(str(self.name) + " error "+ str(self.seen[x]))


    def create_edge_all(self, ir):
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(str(self.name) + " create_edge_all " +ir.prettyprint())


        newedges = super(MyRunStateChallengeOlga,self).create_edge_all(ir)

        logger.debug(str(self.name) + "super(MyRunStateChallengeOlga,self).create_edge_all(ir):" + str(newedges))


        r = ir
        Innext = None
        v = r.getKnownChordInNoteMap()
        In = v.innote
        if hasattr(In, "next"):
            Innext = In.next

        # add wrong node at UnKnown
        # None in the sense of mess


        if (r.getKnownChord() is theUnknownChord)  and Innext:
            rnew = r.extend()

            # we have wrong and jump2unknown without a run?
            # leads to jump2unknown, wrong, jump2unknown on a wrong note ..
            #rnew.knownChordInNoteMap = self.createKnownChordPos(Innext, None, None)

            rnew.knownChordInNoteMap = self.createKnownChordPos(Innext, theUnknownChord, None)

            rnew.minRightSpeedRunState=rnew
            rnew.maxRightSpeedRunState=rnew
            #rnew.updateRunSpeed(# )

            #rnew.errors.append(Jump2UnKnown())

            # isnt persistent, myadd_node clears errors on recalculation
            rnew.errors.append(Wrong())

            rnew = self.myadd_node(rnew)

            self.add_edge(r, rnew, str="wrong at Unknown" + str([str(r.getCurrent2RunSpeed())[0:5], str(rnew.getCurrent2RunSpeed())[0:5]]), weight=rnew.costs())
            #self.add_edge(v,tmp,str="Transpose out Chord Timming Good "+ str([rmid, tmpr.getCurrent2RunSpeed()]), weight=0)
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug( str(self.name) + " adding  wrong at unknown " + str(id(rnew)) + " " + rnew.prettyprint())
            else:
                logger.debug( str(self.name) + " adding wrong at unknown " + str(id(rnew)) + " " + rnew.errorstr)

        else:
            if newedges == 0 or len(r.errors) >0:

            #if newedges == 0:
                if r.getKnownChord is theUnknownChord:
                    print "TheUnknownChord infinity loop\n"
                    1/0


                r = ir
                Innext = None
                v = r.getKnownChordInNoteMap()
                In = v.innote
                if hasattr(In, "next"):
                    Innext = In.next
                rnew = r.extend()
                rnew.knownChordInNoteMap = self.createKnownChordPos(In, theUnknownChord , None)
                rnew.minRightSpeedRunState=rnew
                rnew.maxRightSpeedRunState=rnew
                #rnew.updateRunSpeed(# )

                #rnew.errors.append(Jump2UnKnown())
                #pdb.set_trace()
                rnew = self.myadd_node(rnew)

                rnew.errorstr="jump Back"

                #self.add_edge(v,tmp,str="Transpose out Chord Timming Good "+ str([rmid, tmpr.getCurrent2RunSpeed()]), weight=0)

                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug( str(self.name) + " adding jump2 unknown" + str(id(rnew)) + " " + rnew.prettyprint())
                else:
                    logger.debug( str(self.name) + " adding jump2 unknown" + str(id(rnew)) + " " + rnew.errorstr)

                """
                if self.pushNode(rnew, rnew.rcost):
                    logger.debug( str(self.name) + " pushed " + str(id(rnew)) + " " + rnew.errorstr)
                else:
                    logger.debug( str(self.name) + " NOT pushed " + str(id(rnew)) + " " + rnew.errorstr)
                """

                self.add_edge(r, rnew, str="out Chord" + str([str(r.getCurrent2RunSpeed())[0:5], str(rnew.getCurrent2RunSpeed())[0:5]]), weight=rnew.costs())

                # push because r is proccessed at the moment..
                if self.pushNode(rnew,rnew.rcost) is False:
                    pass
                    #print "push rejected"
                    #code.interact(local=locals())



    def myadd_node(self,anode):
        rnew = anode
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug( str(self.name) + " myadd_node adding " + str(id(rnew)) + " " + rnew.prettyprint())
        else:
            logger.debug( str(self.name) + " myadd_node adding " + str(id(rnew)) + " " + rnew.errorstr)
        return super(MyRunStateChallengeOlga,self).myadd_node(anode)



    def add_note(self, aNote):
        self.innotes.append(aNote)
        self.bestRunOnIn[self.innotes[-1]]=PriorityQueue(key=lambda x: x.rcost[0:2], maxitems=1)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug( str(self.name) + " added new note" + aNote.prettyprint())



    def create_idontknowwhereyouare(self, aIn=None, push =True, costs=None):
        return super(MyRunStateChallengeOlga,self).create_idontknowwhereyouare(aIn=self.innotes[-1])
