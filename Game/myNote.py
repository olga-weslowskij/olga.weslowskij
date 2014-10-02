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

#from dataBase import db


#import dataBase

from mylibs.myPersistent import PersistentObject
import myglobals


XMLMyNotes= Element("MyNotes")

NoteNames  = ['pre start', 'C#-1', 'D-1', 'E--1', 'E-1', 'F-1', 'F#-1', 'G-1', 'G#-1', 'A-1', 'B--1', 'B-1', 'C0', 'C#0', 'D0', 'E-0', 'E0', 'F0', 'F#0', 'G0', 'G#0', 'A0', 'B-0', 'B0', 'C1', 'C#1', 'D1', 'E-1', 'E1', 'F1', 'F#1', 'G1', 'G#1', 'A1', 'B-1', 'B1', 'C2', 'C#2', 'D2', 'E-2', 'E2', 'F2', 'F#2', 'G2', 'G#2', 'A2', 'B-2', 'B2', 'C3', 'C#3', 'D3', 'E-3', 'E3', 'F3', 'F#3', 'G3', 'G#3', 'A3', 'B-3', 'B3', 'C4', 'C#4', 'D4', 'E-4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'B-4', 'B4', 'C5', 'C#5', 'D5', 'E-5', 'E5', 'F5', 'F#5', 'G5', 'G#5', 'A5', 'B-5', 'B5', 'C6', 'C#6', 'D6', 'E-6', 'E6', 'F6', 'F#6', 'G6', 'G#6', 'A6', 'B-6', 'B6', 'C7', 'C#7', 'D7', 'E-7', 'E7', 'F7', 'F#7', 'G7', 'G#7', 'A7', 'B-7', 'B7', 'C8', 'C#8', 'D8', 'E-8', 'E8', 'F8', 'F#8', 'G8', 'G#8', 'A8', 'B-8', 'B8', 'C9', 'C#9', 'D9', 'E-9', 'E9', 'F9', 'F#9', 'G9']

class MyNote(PersistentObject):
    nid=None
    session=None


    def __init__(self, anid=None):

        self.nid = anid
        PersistentObject.__init__(self)

        if self.nid is None:
            self.nid=myglobals.persistent.getId()


        self.persistentexception.extend(["last","next","pos","chord","dbloc"])

        self.dbloc = None
 
        # caches
        self._midi=None
        self._volume=None
        self._myoffset=None
        self._myduration=None


        self._prettyprint=None

    def clone(self):
        ret = MyNote()
        #ret.dbloc = self.dbloc

        ret.midi = self.midi
        ret.volume = self.volume
        ret.myoffset = self.myoffset
        ret.myduration = self.myduration
        return ret

        

    def __str__(self):
        return ", ".join(map(str,[self.nid,self.midi,self.prettyprint(), self.myduration, self.volume ]))



    def noteName(self):
        return NoteNames[self.midi]

    def prettyprint(self):
        if self.midi:
            return ", ".join(map(str,[NoteNames[self.midi], self.myoffset]))
            #n.midi = self.midi
        else:
            return "None"

        #return repr(", ".join(map(str,[n.nameWithOctave])))


    def __repr__(self):
        return repr(self.nid)
        return repr((self.prettyprint() ,repr(self.nid)))

        #return ", ".join(map(str,[n.nameWithOctave, self.myoffset]))
        #return ", ".join(map(str,[self.nid,n.nameWithOctave, self.volume, self.myoffset,self.myduration]))

    def midiEvent(self, abstimetick, speed):
        abstimetick2 = abstimetick
        myspeed = 1/speed
        #print "midievent timetick "+ str(abstimetick)
        #tts = ((60.0*1000000.0/bpm)/resolution)/1000.0
        tts = 1
        tick = int((myspeed * int(self.myoffset/tts)) + abstimetick2)
        #tick = int(myspeed * (int(self.myoffset/tts) + abstimetick2))
        dtick = int(myspeed * (int(self.myduration/tts)))

        tmpev=[[144,self.midi, self.volume],tick]
        tmpev2=[[144,self.midi, 0],tick+dtick]


#        tmpev=pmidi.NoteOnEvent()
#        tmpev.channel=1
#        tmpev.tick=tick
#        tmpev.pitch=self.midi
#        tmpev.velocity=self.volume
#
#
#        tmpev2=pmidi.NoteOffEvent()
#        tmpev2.channel=1
#        tmpev2.tick=dtick +tick
#        tmpev2.pitch=self.midi
#        tmpev2.velocity=self.volume


        return [tmpev,tmpev2]






    @property
    def midi(self):
        if self._midi:
            return self._midi
        #print "midi get\n"
        else:
            self._midi=1
        return self._midi


    @midi.setter
    def midi(self, value):
        self._midi = value
        # why?
        #self.prettyprint()

    @property
    def volume(self):
        if self._volume:
            return self._volume
        self._volume = 1
        return self._volume


    @volume.setter
    def volume(self, value):
        #print "volume set\n"
        self._volume = value

    @property
    def myoffset(self):
        if self._myoffset:
            return self._myoffset
        self._myoffset = float("1")
        return self._myoffset


    @myoffset.setter
    def myoffset(self, value):
        self._myoffset = value

    @property
    def myduration(self):
        if self._myduration:
            return self._myduration
        self._myduration = float("1")
        return self._myduration


    @myduration.setter
    def myduration(self, value):
        self._myduration = value


    def toXml(self, myret):
        myret.write("<MyNote>")
        myret.indent()
        myret.write("<nid>%s</nid>"%(self.nid))
        myret.write("<midi>%s</midi>"%(self.midi))
        myret.write("<velocity>%s</velocity>"%(self.velocity))
        myret.write("<myoffset>%s</myoffset>"%(self.myoffset))
        myret.write("<myduration>%s</myduration>"%(self.myoffset))
        myret.dedent()




class MyPlayedNote(MyNote):
    def __init__(self, *args, **kwargs):
    #def __init__(self, anid=None):
        #super(MyPlayedNote, self).__init__(self, *args, **kwargs)
        MyNote.__init__(self, *args, **kwargs)
        #anid=kwargs.get("anid", None)
        #super(MyPlayedNote,self).__init__()
        #PersistentObject.__init__(self)
        #self.nid = anid
        """
        self.timepressed=None
        self.timereleased=None
        self.pitch=None
        self.velocity=None

        self.known=False
        self.hand=None

        # caches
        self._midi=None
        self._volume=None
        self._myoffset=None
        self._myduration=None

        self.dbloc="playedNotes"


        if self.nid is None:
            if not dataBase.usenodb:
                count  = db.execute("xquery fn:doc('database')/root/%s/count/text()"%(self.dbloc))
                ncount = str(int(count)+1)


                #globalnid = globalnid +1
                ncount = globalnid

                stmt = "xquery replace value of node fn:doc('database')/root/%s/count with %s"%(self.dbloc, ncount)
                db.execute(stmt)

                stmt = "xquery insert node <MyNote><nid>%s</nid><midi/><volume/><myoffset/><myduration/></MyNote> as last into fn:doc('database')/root/%s"%(ncount,self.dbloc)
                db.execute(stmt)
                self.nid = ncount
                self.nid = myglobals.persistent.getId()
        """

        
class MyKnownNote(MyNote):
    #def __init__(self, anid=None):
    def __init__(self, *args, **kwargs):
        #anid=kwargs["anid"]
        #anid=kwargs.get("anid", None)
        #self.nid = anid
        #MyNote.__init__(self)
        #super(MyKnownNote,self).__init__(self, *args, **kwargs)
        MyNote.__init__(self, *args, **kwargs)

        #print "MyKnownNote " + str(self.nid)
        self.hand=None

        """
        # caches
        self._midi=None
        self._volume=None
        self._myoffset=None
        self._myduration=None
        """

        self.dbloc="knownNotes"

        #super(MyKnownNote,self).__init__()

        def prettyprint(self):
            return super(MyKnownNote, self).prettyprint() + " " + str(self.pos)




    #def load(self):


class MessNote(MyKnownNote):
    def __str__(self):
        return "Mess"

    def prettyprint(self):
        return "Mess"

    def noteName(self):
        return self.prettyprint()


class UnknownNote(MyKnownNote):
    def __str__(self):
        return "UnknownNote"

    def noteName(self):
        return self.prettyprint()

    def prettyprint(self):
        return "???"

theUnknownNote= UnknownNote()
theMessNote= MessNote()




if __name__ == "__main__":
    try:
        b = {}

        for x in range(128):
            a = MyKnownNote()
            a._midi=x
            b[x]= a.prettyprint()

        print b.values()

        #print a.nid


        #a = MySong()
        #a.frommusic21('cuae2h.xml')
        #a.frommusic21('ame.xml')
        #a.save()







        #o = MyMidiOut()

        #maxnotes = len(a.mystream.notes)*3/4
        #print maxnotes

        #print a.mystream.prettyprint()
        #maxnotes = 525

        #o.playpartMyStream(a.mystream.notes,0,maxnotes)


        """
        for tmp in a.mystream.chordify():
            for tmp2 in tmp:
                print str(tmp2.midi) +" ",

            print "\n"
        """
        """
        while True:
            #print o.seq.queue_eventlen()
            pass
        """

    except IOError as e:
        # print exception
        print e


