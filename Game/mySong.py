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
from xml.etree.ElementTree import Element

#from music21 import converter, stream, metadata, tempo

from mylibs.myPersistent import PersistentObject
from Game.myStream import MyStream


import myglobals


XMLMySongs= Element("MySongs")

class MySong(PersistentObject):
    def __init__(self):
        self.musicxmlString=None
        self.nid = myglobals.persistent.getId()
        self.mystream = MyStream()
        self.handparts=[]
        PersistentObject.__init__(self)
        self.persistentexception.append('myparts')


        # TODO
        self.startparts=[]
        self.endparts=[]


    def __repr__(self):
        return repr(self.nid)

    def getLevelPos(self, aNote):
        #print("aNote.pos " + str(aNote.pos))
        if len(self.endparts) !=  len(self.startparts):
            print("len(self.endparts) !=  len(self.startparts)")

        if len(self.endparts) ==0:
            if len(self.mystream)==0:
                return None
            else:
                return None

        # find first pos > than aNote.pos
        for i,x in enumerate(self.endparts):
            if x > aNote.pos:
                #print("aNote.pos i " + str(aNote.pos) + " "+  str(i))
                return i
        return -1


    def getLevelEndNote(self, aNote):
        try:
            return self.mystream[self.endparts[self.getLevelPos(aNote)]]
        except:
            return None

    def getLevelEndNoteNr(self, nr):
        try:
            return self.mystream[self.endparts[nr]]
        except:
            return None


    def getLevelStartNote(self, aNote):
        try:
            return self.mystream[self.startparts[self.getLevelPos(aNote)]]
        except:
            return None

    def getLevelStartNoteNr(self, nr):
        try:
            return self.mystream[self.startparts[nr]]
        except:
            return None


    def fromXml2(self, tree, nid=None):
        super(MySong, self).fromXml2(tree, nid)
        self.mystream = self.mystream.decorate()
        self.mystream.song = self



if __name__ == "__main__":
    try:
        a = MySong()

        a.fromXml2file("../Songs/OlgaXml/Chopin284small.xml")

    except IOError as e:
        # print exception
        print e