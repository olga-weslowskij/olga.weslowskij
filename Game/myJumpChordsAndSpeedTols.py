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
from Game import myStream

from Game.myStream import MyStream
from mylibs.myUniqueList import MyUniqueList


def note2repr(tmp):
    ret = None
    try:
        ret = tmp.midi
    except:
        pass
    return ret


class MyJumpChordsAndSpeedTols(object):
    def __init__(self):
        self.notes=MyStream()
        # self.streams=[]
        self.chordMap={}
        self.knownStreams = MyUniqueList()

    def __getitem__(self, item):
        return self.notes[item]

    def registerNote(self,aNote, speed, aspeedtol):

        if aNote.mystream:
            self.knownStreams.append(aNote.mystream)
        tmp=aNote
        if tmp.chord:
            index = self.chordMap.get(str(note2repr(tmp)),[])
            if not tmp.chord in index:
                index.append((tmp.chord, speed, aspeedtol))
                self.chordMap[str(note2repr(tmp))] = index

                #print tmp.prettyprint() + " registered"
        else:
            print "how to register undecorated stream?"


    def getChords(self, aNote):
        ret  = self.chordMap.get(str(note2repr(aNote)),[])
        #print "len(ret) " + str(len(ret))
        #code.interact(local=locals())
        return ret



    def registerStream(self, stream, speed, aspeedtol):
        for x in stream:
            self.registerNote(x, speed, aspeedtol)
