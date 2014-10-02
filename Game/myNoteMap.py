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

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ +  '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)


def sortnid(a):
    return a.nid

class NoteMap(object):
    pass

width=200
height=150

class KnownChordPos(object):
    def __init__(self):
        # bad innote is used to display and as position and identification
        self._innote = None
        self._knownChord = None

        self._knownNote=None

        self.innotes = None
        self.innotespos=None

        self.playedChordNotesgood=[]
        self.innotesWrong = []

        #self.playedChordNotes = []
        self.cost = ""

        self._repr = None
        self._str = None

    def __str__(self):
        if self._str is None:
            self._str =  str([self.knownChord, self.innote]) + " " + str(self.playedChordNotesgood) + " " + str(self.cost)
        return self._str

        """
        if costonedgedict.has_key(self):
            return str([self.innote.pos, self.knownote.pos]) + " " + str(costonedgedict[self]) + "\n" + str(
                (self.innote, self.knownote)) + str(self.playedChordNotes)
        return str([self.innote.pos, self.knownote.pos]) + " " + str(self.cost)
        """


    def prettyprint(self):
        txt=""

        try:
            si = self._innote.prettyprint()
        except:
            si = str(self._innote)

        """
        try:
            sk = self._knownChord.prettyprint()
        except:
            sk = str(self._knownChord)
        """

        sk ="["
        for n in self.playedChordNotesgood:
            sk = sk + n.prettyprint() +", "

        sk = sk +"]"
        try:
            for n in self._knownChord:
                if n not in self.playedChordNotesgood:
                    sk = sk + "-" + n.prettyprint() +","
        except:
            sk = str(self._knownChord)


        return si + " -> " + sk


    def __repr__(self):
        return self.myrepr()
        #return self.__str__()


    """
    def extend(self, anote):
        ret = copy.copy(self)

        K = self._knownChord

        ret._innote = anote
        # always append ??


        note = K.getChordtonesofType(anote)

       # already played ??
        skip = False
        for note in ret.playedChordNotesgood:
            if note is K:
                skip = True

        if not skip and True:
            if K:
                #logger.debug("appending " + K.prettyprint() + " to " + str(id(ret.playedChordNotes)))
                #ret.playedChordNotes.append(K)

                if True:
                    if note:
                        ret.knownnote = note
                        ret.playedChordNotesgood.append(ret.knownnote)
                    else:
                        # innote not in chord
                        ret.knownnote = None
                        ret.innotesWrong.append(anote)


        else:
            # innote already played
            ret.innotesWrong.append(anote)

        return ret

    """


    @property
    def knownnote(self):
        if self._knownNote:
            return self._knownNote
        else:
            #missing = list(set(self._knownChord) - set(self.playedChordNotesgood))
            #if len(missing) > 0:
            #    return missing[0]
            #else:
            return None

    @knownnote.setter
    def knownnote(self, k):
        self._knownNote = k


    @property
    def innote(self):
        return self._innote

    @innote.setter
    def innote(self,a):
        self._innote = a


    @property
    def knownChord(self):
        return self._knownChord

    @knownChord.setter
    def knownChord(self,a):
        self._knownChord = a


    def myrepr(self):
        if self._repr is None:
            a = sorted(self.playedChordNotesgood, key=sortnid)

            #self._repr = str([self.knownote.nid, getattr(self.innote,"nid",None), a])
            # why len(self.innotesWrong)
            #tmp = str([getattr(self.knownote, "nid", None), getattr(self.innote, "nid", None), a, len(self.innotesWrong)])

            # it doesnt matter wheter the error is explicit via edges or implicit via Wrong

            #print str(self.__dict__)

            kchord = repr(None)
            if not(self._knownChord is None):
                kchord = repr(self._knownChord)

            #print "kchord: " + str(kchord)
            #tmp = str([getattr(self.knownote, "nid", None), getattr(self.innote, "nid", None), a])
            tmp = str([kchord, getattr(self.innote, "nid", None), a])

            if self._repr and tmp != self._repr:
                print "caching error!\n"+ tmp + " vs " + self._repr

            self._repr = tmp

        #b = sorted(self.missingChordNotes,key=sortnid)
        #print "myrepr", self._repr
        return self._repr

    def chordfull(self):
        if self._knownChord:
            return len(self.playedChordNotesgood) + len(self.innotesWrong) == len(self._knownChord)
        else:
            return False


    def drawpos(self, drawposdict):
        maxoffset= 8

        if self.knownChord:
            kpos = self.knownChord.notes[0].pos
        else:
            kpos = -1

        if hasattr(self.innote,"pos"):
            ipos = self.innote.pos
        else:
            ipos = -1

        key = str([kpos * width, ipos * (height)*maxoffset])


        #print "drawpos key " + str(key)

        if drawposdict.has_key(key):
            drawposdict[key] = drawposdict[key] + 1
        else:
            drawposdict[key] = 0


        offset = drawposdict[key]


        return [kpos * width + (offset * 10), (ipos * (height*maxoffset)) + (offset * height)]


    def activeKnownChord(self):
        if self._knownChord is None:
            return None
        if self.chordfull():
            if hasattr(self._knownChord, "nextChord"):
                return self._knownChord.nextChord
            else:
                return None
        else:
            """
            for anote in self.knownChord.notes:
                if not (anote in self.playedChordNotesgood):

            """
            return self._knownChord

    def nextInNote(self):
        return self.innotes[self.innotespos+1]

