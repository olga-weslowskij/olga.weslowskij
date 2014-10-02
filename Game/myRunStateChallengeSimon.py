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
import pdb
from Game.myLevenshteinChallenge import MyLevenshteinChallenge
from Game.myNote import theUnknownNote
from Game.myRunStateChallenge import MyRunStateChallenge
from mylibs.priorityQueue import PriorityQueue

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
#logger.setLevel(logging.DEBUG)
logger.setLevel(logging.NOTSET)
logger.setLevel(logging.INFO)

class MyRunStateChallengeSimon(MyRunStateChallenge):
    def __init__(self):
        super(MyRunStateChallengeSimon, self).__init__()

        # why not init here
        self.myinit()


        # knownchord.pos would be better
        self.nofollower={}

    def add_note(self, aNote):
        if self.name is None:
            self.myinit()

        super(MyRunStateChallengeSimon,self).add_note(aNote)
        self.newnote = True

        # create new starts
        self.create_idontknowwhereyouare(aIn=self.innotes[-1])
        self.newnote = True

    def myinit(self):
        if self.name != "RunStateSimon":
            self.name = "RunStateSimon"
            #pdb.set_trace()
            self.add_note(theUnknownNote)



            super(MyRunStateChallengeSimon,self).create_idontknowwhereyouare(aIn=self.innotes[-1])


    def update(self):
        if self.name is None:
            self.myinit()

        super(MyLevenshteinChallenge, self).update()
        #super(MyRunStateChallengeOlga, self).update()

        if self.newnote and logger.isEnabledFor(logging.DEBUG):
            self.newnote = False
            logger.info( str(self.name) + " all noNextInNoteMappings " + self.innotes[-1].prettyprint())
            for x in self.noNextInNoteMappings.keys():
                logger.info( str(self.name) + x.prettyprint())
                logger.info(str(self.name) + " error "+ str(self.seen[x]))

        if self.newnote and logger.isEnabledFor(logging.INFO):
            logger.info(self.bestRunOnIn[self.innotes[-1]].peek().prettyprint())





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

        # no follower
        # same Future

        if r.lastfullchordRun or True:

            if r.speedtol != 0.0:
                pkey = str([repr(r.knownChordInNoteMap),r.rspeed()])
            else:
                pkey = str([repr(r.knownChordInNoteMap)])

            if self.nofollower.has_key(pkey):
                p = self.nofollower[pkey]

                """
                if p.key(p.peek()) > p.key(r):
                    print "living Bastard\n"
                """


                p.add(r)

                #if not(p.peek() is  r):
                if not(p.has_item(r)):
                    logger.debug(str(self.name) + " " + "..cutted")
                    return True

            else:
                p = PriorityQueue(key=lambda x: (x.rcost, -x.lenlist), maxitems=1)

                self.nofollower[pkey] = p
                p[r]=r


            """
            # debug TODO erase me

            if r.getKnownNote() and r.getKnownNote().myoffset == 65545:
                 code.interact(local=locals())
            """
        return False

