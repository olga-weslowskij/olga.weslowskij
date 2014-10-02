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
import heapq
#from Requests.ShowErrors import createShowErrorStream
#from chordMapIndex import chordMap, chord2repr
#import main
from Game.noNextInNoteSet import NoNextInNoteSet

from mylibs.myDict import MyDict
#import matplotlib.pyplot as plt

import hotshot


logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
#logger.setLevel(logging.DEBUG)
logger.setLevel(logging.NOTSET)


prof_enabled = False

if prof_enabled:
    prof = hotshot.Profile(__name__ + ".prof")


class incDijkstra(object):
    def __init__(self):
        self.seen = {}
        self.fringe = []
        #heapq.heappush(self.fringe,(0,self.source))

        self.elabels = {}
        self.noNextInNoteMappings = NoNextInNoteSet()

        self.pos = MyDict()
        self.pos.defaultvalue=(0,0)


    def target_reached(self, v):
        return False

        #self.Gtmp.add_edge(tmp.inwortStartIndex,tmp.inwortStartIndex+tmp.len, Intervall=tmp)

    def add_edge(self, v, w, **dicts):

        self.G.add_edge(v, w, **dicts)

        #self.pos[v]=v.drawpos()
        #self.pos[w]=w.drawpos()

        #print self.pos

        #print "add_edge", self.G[v][w][0]
        self.elabels[(v, w)] = self.G[v][w][0]['str']

        #print self.elabels
        # dicts[str]
        # pushknots only once, gets reset on update (dikjstra)

        #We only call add_edge on the fly atm
        """
        if self.pushknots.get(v,True):
            self.pushknots[v]=False
            if self.seen.has_key(v):
                heapq.heappush(self.fringe,(self.seen[v],v))
                """


    #def create_start_notes(self):
    #        pass

    def create_edge_fly(self, v):
        print "flying ", v
        print "edges before fly", self.G.edges()
        print "edges after fly", self.G.edges()
        return


    def draw(self):
        #networkx.draw(self.G,self.pos)
        #networkx.draw_networkx(self.G, self.pos)#,with_labels=True, labels= test.elabels)
        """
        networkx.draw_networkx(self.G, self.pos,with_labels=False)#, labels= test.elabels)
        networkx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=self.elabels)
        plt.show()
        """


    def postupdate(self):
        pass

    def errorcut(self,r):
        return False
        pass

    def update(self):
        """Compute shortest paths and lengths in a weighted graph G.

        Uses Dijkstra's algorithm for shortest paths.

        """

        #print "enter update"
        if prof_enabled:
            try:
                prof.start()
            except:
                pass


        if logger.isEnabledFor(logging.INFO):
            logger.info("update.enter len(Actives): "  + str(len(self.noNextInNoteMappings.values())))
            #logger.info("update.enter node count " + str(len(self.G.nodes())))
            logger.info("update.enter node count " + str(self.G.number_of_nodes()))

        self.pushknots = {}

        weight = 'weight'


        # repush lastsol
        #if not self.fringe:

        for x in self.noNextInNoteMappings.values():
            heapq.heappush(self.fringe, (self.seen[x], x))

        self.noNextInNoteMappings = NoNextInNoteSet()

        while len(self.fringe) > 0:

            (d, v) = heapq.heappop(self.fringe)
            # just make solutions better discard old solutions wich where improved
            #print "seen ",self.seen

            #



            """
            cut in incdikstra ??
            """
            while self.seen.get(v, d) < d and len(self.fringe) > 0:
                (d, v) = heapq.heappop(self.fringe)
                # logger.info("popping away the history ", v ," ",d , " vs ", self.seen.get(v,d))
            if self.seen.get(v, d) < d:
                break



            #print self.fringe

            #pdb.set_trace()



            #            if v in self.dist:
            #                continue # already searched this node.
            #            self.dist[v] = d

            if not self.errorcut(v):
                logger.debug("target reached")
                if self.target_reached(v):
                #if v == target:
                    #print len(self.echappe), len(self.noNextInNoteMappings)
                    return v
                logger.debug("no")


                #if len(self.echappe) == 0 or not self.echappe.values()[-1] == v:
                # create edges and nodes on the fly


                # get new neighboorhood knot
                # create all Transpose edges
                # create all
                logger.debug(" create_edge entered")
                self.create_edge_fly(v)
                #else:
                #logger.info(" create_edge missed")

            if self.G.is_multigraph():
                edata = []
                for w, keydata in self.G[v].items():
                    minweight = min((dd.get(weight, 1) for k, dd in keydata.items()))
                    #edata.append((w,{weight:minweight}))
                    # we need all edges with weight of minweight
                    for k, dd in keydata.items():
                        if (dd.get(weight, 1) == minweight):
                            dd['weight'] = dd.get(weight, 1)
                            edata.append((w, dd))
            else:
                edata = iter(self.G[v].items())

            for w, edgedata in edata:
                sw_dist = self.seen[v] + edgedata.get(weight, 1)
                self.pushNode(w, sw_dist)



        # all done let me see
        #self.draw()
        #if len(self.echappe.items()) == 0:
             #logger.info("no actives anymore")
        #    self.target_not_reached()
            #self.draw()
        if logger.isEnabledFor(logging.INFO):
            logger.info("update all done len(self.noNextInNoteMappings): " + str(len(self.noNextInNoteMappings)))
            logger.info("node count now " + str(self.G.number_of_nodes()))

        #code.interact(local=locals())
        self.postupdate()

        if prof_enabled:
            prof.stop()
        return None


    def pushNode(self,w , sw_dist):
        if w not in self.seen or sw_dist < self.seen[w]:
            self.seen[w] = sw_dist
            heapq.heappush(self.fringe, (sw_dist, w))
            return True
        return False
        """
        else:
            logger.info(" " + str(id(w)) + " dropped")
            logger.info(" " + str(w) + "")
        """



