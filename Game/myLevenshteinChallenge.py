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


import networkx
from Game import myStream, myNote
from mylibs.incDijksra import incDijkstra
from mylibs.myDict import MyDict
from Game.myKey import mykey
from Game.myJumpChordsAndSpeedTols import MyJumpChordsAndSpeedTols
import logging
from Game.myNoteMap import KnownChordPos


logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ +  '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)
#logger.setLevel(logging.DEBUG)

#prof = hotshot.Profile(__name__ + ".prof")


costonedgedict = {}

chorddetection = myStream.ischordms


class MyLevenshteinChallenge(incDijkstra):
    def __init__(self):
        super(MyLevenshteinChallenge, self).__init__()
        global costonedgedict
        #if G == None:
        self.G = networkx.MultiDiGraph()
        self.drawposdict = MyDict()

        self.drawposdict.defaultvalue=0

        #else:
        #    self.G= G

        self.innotes = myStream.MyStream()
        self.echappei = []

        self.nodes = {}

        self.NoteMaps = {}

        self.jumpToStates = MyJumpChordsAndSpeedTols()



        #self.echappe=[]
        #self.noNextInNoteMappings=[]

        self.cut={}


        self.nodefullexpanded = {}
        self.target_not_reached = self.target_not_reached_and_do

        self.errors = [0,0]
        self.challengestartnote = None

        #self.challengestartnote = self.jumpToStates.notes[0]
        self.challengeendnote = None

        self.challengeendchord = None

        self.maxerror = [1,1]

        self.maxerrorAtKnownnote={}

        self.targets=[]

        self.speedtol = 0.25

        self.donelist = {}

        self.retondone=False

        self.verbosetimming=True

        self.chain=[]


        self.name = None


        # to print values on knots..
        costonedgedict = self.seen


    def challengelen(self):
        start =self.challengestartnote
        if start is None:
            start = self.challengestartchord.notes[0]

        end = self.challengeendnote

        if end is None:
            end = self.challengeendchord.notes[0]

        return end.pos - start.pos


    # depricated ???
    def knownStream(self):
        start =self.challengestartnote
        if start is None:
            start = self.challengestartchord.notes[0]

        end = self.challengeendnote

        if end is None:
            end = self.challengeendchord.notes[0]

        ret = myStream.MyStream()
        ret = ret.buildAllInChordRange(start,end)


        return ret





    """
    def errorcut(self,r):
        m = r.currentMelodyRating
        v = m.notenextMapping
        logger.debug(str(self.name) + " " + "cutting error " + str(self.seen[r]))
        if self.maxerror is not None:
            #if self.seen[r]- r.rcost > self.maxerror:
            #if self.seen[r] > self.maxerror:
            if self.seen[r][0:2] > self.maxerrorAtKnownnote.get(v.knownChord, self.maxerror)[0:2]:

                # just save Notes between start and endnote
                #if v.knownote.pos >= self.challengestartnote.pos:

                #self.cut[r]=r

                logger.debug(str(self.name) + " " + "..cutted")
                return True

        logger.debug(str(self.name) + " " + "not cutted")
        return False

        pass





    def target_reached(self, r):
        #b = (v.innote.__repr__()) == self.target.__repr__()
        #b = v.innote is self.target

        m = r.currentMelodyRating
        v = m.notenextMapping
        if logger.isEnabledFor(logging.DEBUG) and r.lenlist > 1:

            logger.debug(str(self.name) + " " + "checking targets for " + r.prettyprint())

        # check targets

        if len(self.targets) == 0:
            self.targets =[(self.challengeendnote, self.challengeendchord)]

        #logger.debug(str(self.name) + " and targets" + str(self.targets))

        for tnote, tchord in self.targets:
            logger.debug(str(self.name) + " " + "check " + str(tnote)+ tchord.prettyprint())

            if v.knownChord == tnote or (v.knownChord == tchord and v.chordfull()):
                #logger.info("target "+ str((tnote,tchord)) + "reached " + str( self.seen[r]- r.rcost) + " errors")

                a = self.donelist.get((tnote,tchord),[])
                a.append(r)
                self.donelist[(tnote,tchord)]=a

                if self.retondone == (tnote,tchord):
                    logger.debug(str(self.name) + " " + "target reached: ret and done")
                    return True
                logger.debug(str(self.name) + " " + "target reached")

        return False
        #return v == self.target

    """


    def target_not_reached_and_nothing(self):
        pass

    def target_not_reached_and_do(self):
        pass
        #print "check Challenge coding bug"


    def update(self):
        ret = super(MyLevenshteinChallenge,self).update()
        logger.info(str(self.name) + " " + "myLevenshteinChallenge stats")
        logger.info(str(self.name) + " " + "nodes " + str(len(self.nodes)))
        logger.info(str(self.name) + " " + "noNextInNoteMappings " + str(len(self.noNextInNoteMappings)))
        return ret


    #def createKnownChordPos(self, I, K, parent, newplayedchords=None, good=True, appendKnownChord=True):
    def createKnownChordPos(self, I, K, parent, good=True, appendKnownChord=True):
        # create NoteMaps at most once
        ret = KnownChordPos()
        ret.innote = I
        ret.knownChord = K


        if hasattr(K, "myoffset"):
            pass
            #1/0

        if parent is not None:
            #ret.playedChordNotes = list(parent.playedChordNotes)

            ret.innotesWrong = list(parent.innotesWrong)
            ret.playedChordNotesgood = list(parent.playedChordNotesgood)
        else:
            pass
            """
            if K:
                ret.playedChordNotes = [K]
                if good:
                    ret.playedChordNotesgood=[K]
                else:
                    ret.innotesWrong=[I]
            """

        #self.pos[ret]= ret.drawpos()

        # always append ??

        skip = False
        for note in ret.playedChordNotesgood:
            if note is K:
                skip = True

        if not skip and appendKnownChord:
            if K:
                #logger.debug("appending " + K.prettyprint() + " to " + str(id(ret.playedChordNotes)))
                #ret.playedChordNotes.append(K)

                if good:
                    if len(K.getChordtonesofType(I))>0:
                        ret.knownnote = K.getChordtonesofType(I)[0]
                        ret.playedChordNotesgood.append(ret.knownnote)
                    else:
                        ret.knownnote = None
                        ret.innotesWrong.append(I)

                else:
                    ret.innotesWrong.append(I)


        # mess needs to advance In but dont change playedchords..
        #if newplayedchords:
        #    ret.playedChordNotesgood = list(newplayedchords)
            # TODO copy innotesWrong too (Done??)
            #ret.innotesWrong = list()

        #ret2 = self.nodes.get(ret.myrepr())

        if False:


            ret2 = self.NoteMaps.get(ret.myrepr())

            if ret2 is None:
                #self.G.add_node(ret)
                self.NoteMaps[ret.myrepr()] = ret
                #self.pos[ret] = ret.drawpos()
                return ret
            else:
                """
                if justnew:
                    print "justnew Notemaps\n"
                    return None
                """
                return ret2

        return ret


    # more update because of  incoming note
    def add_note(self, aNote):
        print("overwrite me!")
        pass


        # calculate it
        #self.update()


    # todo rewrite
    def findsolution(self, atarget=None):
        if atarget is None:
            btarget = self.targets[-1]
        if len(self.donelist.get(btarget,[]))==0:
            #tmp = MyLevenshteinChallenge()
            tmp = self.__class__()
            tmp.maxerror=None
            tmp.maxerrorAtKnownnote={}
            tmp.retondone= btarget
            tmp.targets = self.targets
            tmp.speedtol=self.speedtol

            # for drawing
            tmp.challengestartnote = self.challengestartnote
            tmp.jumpToStates = self.jumpToStates
            tmp.name= "findsolution"


            for v in self.innotes:
                tmp.add_note(v)
                tmp.update()

            #tmp.draw()

            return (tmp, tmp.donelist[btarget])
        else:
            return (self,self.donelist.get(btarget))

        """
        if atarget is None:
            btarget = self.targets[-1]
        if len(self.donelist.get(btarget,[]))==0:
            #tmp = MyLevenshteinChallenge()
            tmp = self.__class__()
            tmp.maxerror=None
            tmp.maxerrorAtKnownnote={}
            tmp.retondone= btarget
            tmp.fringe = list(self.fringe)
            tmp.targets = self.targets
            tmp.seen = dict(self.seen)
            tmp.nodes = dict(self.nodes)
            tmp.speedtol=self.speedtol

            # for drawing
            tmp.challengestartnote = self.challengestartnote
            tmp.pos=dict(self.pos)
            tmp.drawposdict = dict(self.drawposdict)

            tmp.name= "findsolution"

            tmp.noNextInNoteMappings= NoNextInNoteSet(self.noNextInNoteMappings)

            tmp.NoteMaps = dict(self.NoteMaps)


            for v in self.cut.values():
                d = self.seen[v]
                heapq.heappush(tmp.fringe, (d, v))



            tmp.update()

            #tmp.draw()

            return (tmp, tmp.donelist[btarget])
        else:
            return (self,self.donelist.get(btarget))
            """


    def myadd_edge(self, v, w, **dicts):

        Ipos = (v.innote.pos, v.knownChord.pos)
        Kpos = (w.innote.pos, w.knownChord.pos)

        ret = self.edges.get((Ipos, Kpos), None)

        if ret is None:
            ret = self.edges.get((Kpos, Ipos), None)

        if ret is not None:
            self.add_edge(v, w, dicts)

        pass


    def myadd_node(self,anode):
        """ bad cause errors are permutating (really?)"""
        """

        # no caching
        # jump creates nodes witch arent optimal and then recached on despite better solutions
        self.G.add_node(anode)
        #self.nodes[anode.EqState()]=anode

        self.pos[anode] = anode.currentMelodyRating.notenextMapping.drawpos(self.drawposdict)

        return anode
        """

        #if anode.currentMelodyRating.errorstr=="jump":
        #    print ""
        #    pass

        # caching state Tree != dist tree
        m1t = self.nodes.get(anode.EqState(),None)
        if m1t is None:
            self.G.add_node(anode)
            self.nodes[anode.EqState()]=anode
            #print "added state to tree"
            m1t = anode
            self.pos[m1t] = m1t.currentMelodyRating.notenextMapping.drawpos(self.drawposdict)
            #logger.info(str(id(m1t)) +" currentMelodyRating.notenextMapping" +  str(m1t.currentMelodyRating.notenextMapping.innote.pos))
            #logger.info(str(id(m1t)) +" drawpos " +  str(self.pos[m1t]))
        else:
            m1t = self.nodes.get(anode.EqState())

        return m1t
        #"""



    def farestActive(self):
        if len(self.noNextInNoteMappings.keys())>0:
            return max(self.noNextInNoteMappings.keys(), key = lambda a: a.currentMelodyRating.notenextMapping.knownChord.pos)
        return None

    def longestActive(self):
        if len(self.noNextInNoteMappings.keys())>0:
            #return max(self.noNextInNoteMappings.keys(), key = lambda a: len(a.list))
            return max(self.noNextInNoteMappings.keys(), key = lambda a: a.lenlist)
        return None

    def bestActive(self):
        if len(self.noNextInNoteMappings.keys())>0:
            #return max(self.noNextInNoteMappings.keys(), key = lambda a: (self.seen[a],len(a.list)))
            return max(self.noNextInNoteMappings.keys(), key = lambda a: (self.seen[a],a.lenlist))
        return None





if __name__ == '__main__':
    print "Hallo"


    a=mykey([2,4])

    b=mykey([1,3])

    print a+b
    print a-b

    print mykey([0,0,4])> mykey([0,0])

    print mykey([2,0])> 2

    exit(0)


    myLevenstein = MyLevenshteinChallenge()
    G = myLevenstein.G
    midii = [20, 30, 40, 50, 60]

    perm = [2, 3, 1, 4]

    midik = [midii[0]]

    for i in perm:
        midik.append(midii[i])

    #Error
    midik[3] = 55

    #midik.reverse()

    K = []
    I = []
    i = 0

    for x in range(len(midii)):
        a = KnownChordPos()

        ab = myNote.MyNote()
        ab.midi = midii[x]
        ab.myoffset = 100
        ab.last = None
        ab.next = None
        ab.pos = i

        if len(K) > 0:
            ab.last = K[-1]
            K[-1].next = ab

        K.append(ab)

        bb = myNote.MyNote()
        bb.midi = midik[x]
        bb.myoffset = 200
        bb.last = None
        bb.next = None
        bb.pos = i
        #print bb

        if len(I) > 0:
            bb.last = I[-1]
            I[-1].next = bb

        I.append(bb)

        i = i + 1

    s = KnownChordPos()
    s.knownChord = K[0]
    s.innote = I[0]
    print s

    #test= incDijkstra(G,s)
    G.add_node(s)
    #G.add_node("s")
    test.pos[s] = [0, 0]

    for x in I[1:len(I)]:
        print "test.G.nodes ", test.G.nodes()
        print "test.G.edges ", test.G.edges()

        test.target = x
        mytmp = x.next
        x.next = x.next

        print "test.target", test.target.__repr__(), "test.source", test.source.innote.__repr__()
        print test.update()
        x.next = mytmp




        #networkx.draw(G,{s:[10,10],"s":[0,0]})
        networkx.draw(G, test.pos)
        networkx.draw_networkx(G, test.pos)#,with_labels=True, labels= test.elabels)
        networkx.draw_networkx_edge_labels(G, test.pos, edge_labels=test.elabels)
        #networkx.draw_networkx_edge_labels(G, test.pos)
        #networkx.draw_networkx_edge_labels(G)
        plt.show()

    print I
    print K
