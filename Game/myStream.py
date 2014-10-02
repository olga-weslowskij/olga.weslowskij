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
import random
import time
from Game import options
from Game.myKnownChord import MyKnownChord
from mylibs.myList import MyList

from Game.myNote import MyKnownNote, MyNote
from mylibs.myPersistent import PersistentObject
import myglobals




ischordms = 100


class MyStream(PersistentObject):
    def __init__(self):
        PersistentObject.__init__(self)
        self.notes=MyList()

        self.notes.dog_class = MyNote

        self.song=None
        self.persistentexception.append("song")
        self.hands=None


        self.nid=myglobals.persistent.getId()



    """
        # TODO
        self.startparts=[]
        self.endparts=[]

    def getLevelEndNote(self, aNote):
        if len(self.endparts) ==0:
            if len(self.notes)==0:
                return None
            else:
                return self.notes[-1]

        for x in self.endparts:
            if x.pos > aNote.pos:
                return x

    def getLevelStartNote(self, aNote):
        if len(self.startparts) ==0:
            if len(self.notes)==0:
                return None
            else:
                return self.notes[-1]

        for x in self.startparts:
            if x.pos > aNote.pos:
                return x
            """


    def __getitem__(self, item):
        return self.notes[item]

    def __len__(self):
        return self.notes.__len__()

    def __iter__(self):
        return self.notes.__iter__()

    def __repr__(self):
        #return self.nid
        return repr(self.nid)

    """
    def toXml2(self, tree):
        song = SubElement(tree, self.__class__.__name__)
        song.attrib["nid"]= repr(self.nid)
        window = song
        # SubElement(song, str(self.nid))
        titles = self.__dict__.iterkeys()
        for title in titles:
            o = self.__getattribute__(title)
            # exceptions
            if o is self.song:
                newtitle = SubElement(window, str(title))
                newtitle.text = repr(o)
                continue
            if hasattr(o, "toXml2"):
                o.toXml2(window)
            else:
                newtitle = SubElement(window, str(title))
                newtitle.text = repr(o)


    def fromXml2(self, nid, tree):
        #tree.parse("index.xhtml")
        self.nid = nid
        p = tree.find(str(nid))
        for child in p:
            self.__setattr__(str(child.tag), ast.literal_eval(child.text))
    """

    def build(self, start, end):
        tmp = start
        self.append(tmp)
        #ret = [tmp]
        while hasattr(tmp,"next"):
            if tmp is end:
                break
            tmp = tmp.next
            self.append(tmp)

        return self

    def buildList(self, start,end):
        tmp = start
        ret = []
        ret.append(tmp)
        #ret = [tmp]
        while hasattr(tmp,"next"):
            if tmp is end:
                break
            tmp = tmp.next
            ret.append(tmp)
        return ret



    def buildAllInChordRangeList(self, start, end):
        #ret = MyStream()
        ret = []
        #ret.song = self.song

        tmp= start
        while(start.myoffset-ischordms > tmp.myoffset):
            tmp=tmp.last

        if tmp.myoffset-ischordms < end.myoffset:
            b = ret.append(tmp)

        while (hasattr(tmp,"next") and tmp.next.myoffset-ischordms < end.myoffset):
            tmp=tmp.next
            b = ret.append(tmp)



        #dret = ret.decorate()

        #print("buildAllInChordRange ")
        #for x in dret.notes:
        #    print(str(x.note))

        return ret




    def buildAllInChordRange(self, start, end):
        #print("buildAllInChordRange ") + str([start.note,end.note])
        ret = MyStream()
        ret.song = self.song

        for x in self.buildAllInChordRangeList(start,end):
            ret.append(x)
        dret = ret.decorate()

        #print("buildAllInChordRange ")
        for x in dret.notes:
            pass
            #print(str(x.note))
            str(x.note)

        return dret



    def prettyprint(self):

        ret = "\n".join([str(x) for x in self.notes])
        return ret


    def sort(self):
        def amysort(a):
            #print a
            return a.myoffset

            #for tmp in self:
            #print tmp
        #self.sort(key=amysort)
        self.notes = MyList(sorted(self.notes,key=amysort))
        self.notes.dog_class = MyNote
        return self


    def getHand(self,  hand):
        ret =MyStream()
        ret.song= self.song
        ret.hands= self.hands

        for tmp in self.notes:
            if tmp.hand in hand:
                ret.append(tmp)
        return ret



    def splitChords(self):
        tmpstream= MyStream()

        #Arpeggio
        start = 0
        delay = 500
        streamchord=self.chordify()
        for i in xrange(len(streamchord)):
            for y in (streamchord[i]):
                x=y.clone()
                tmpstream.append(x)
                x.myoffset = start
                x.myduration=delay
                start +=delay

            # new chord offset
            if i > 0:
                start = start + streamchord[i][0].myoffset - streamchord[i-1][0].myoffset

        return tmpstream



    def chordify(self):
        ret =MyList()
        ret.song= self.song
        ret.hands= self.hands


        chord=[]
        chord=MyKnownChord()
        for tmp in self.notes:
            if len(chord) ==0:
                chord.append(tmp)
            else:
                if abs(chord[0].myoffset - tmp.myoffset) < ischordms:
                    chord.append(tmp)
                else:
                    schord = sorted(chord,key=lambda x: x.midi)
                    ret.append(schord)
                    chord = [tmp]
        if len(chord)>0:
            schord = sorted(chord,key=lambda x: x.midi)
            ret.append(schord)
        return ret




    def frommusic21(self, m21stream,bpm,hand):
        #print "frommusic21 stream" + str(len(m21stream.flat.notes))
        #for tmp in m21stream.flat.notes:
        for tmp in m21stream:
            if tmp.isChord:
                #print "append chord" + str((tmp.offset *60.0/bpm)*1000)
                for tmp2 in tmp:
                    kNote = MyKnownNote()

                    kNote.midi=tmp2.midi
                    kNote.myoffset =(tmp.offset *60.0/bpm)*1000
                    #kNote.myduration=((tmp2.duration.quarterLength*60.0/bpm)*1000)
                    kNote.myduration=((tmp.duration.quarterLength*60.0/bpm)*1000)

                    if tmp2.volume.velocity:
                        kNote.volume=tmp2.volume.velocity
                    else:
                        kNote.volume= options.getOptionValue("midi.volume")


                    kNote.hand=hand
                    #print "append(kNote)" + str(kNote)
                    self.append(kNote)
                    #print "append chord done"
            else:
                if tmp.isNote:
                    kNote = MyKnownNote()
                    kNote.midi=tmp.midi
                    kNote.myoffset =tmp.offset *(60.0/bpm)*1000
                    kNote.myduration=(tmp.duration.quarterLength*(60.0/bpm)*1000)
                    if tmp.volume.velocity:
                        kNote.volume=tmp.volume.velocity
                    else:
                        kNote.volume= options.getOptionValue("midi.volume")
                    kNote.hand=hand
                    #print "append(kNote)" + str(kNote)
                    self.append(kNote)


    def shift(self, amount):
        for x in self:
            x.myoffset = x.myoffset + amount
        return self


    def appendStream(self, stream , shift = None, pause = 0, speed =1):
        if shift is None:
            myshift = 0
            if len(self) > 0:
                myshift = self[-1].myoffset + self[-1].myduration
        else:
            myshift = shift

        for y in stream:
            x=y.clone()
            # no dirty detection
            #x.myoffset = x.myoffset + myshift + pause
            x.myoffset = (x.myoffset*speed) + myshift + pause
            self.append(x)
            # was here
            #x.myoffset = (x.myoffset*speed) + myshift + pause

            #x.myoffset = x.myoffset + myshift + pause

        return self

    def extend(self,a):
        for x in a:
            self.append(x)

    def append(self,a):
        #print "MyStream append " +str(a)

        # unpacking note
        tmp = a
        while hasattr(tmp,"note"):
            tmp = tmp.note

        b = MyStreamNoteItem(tmp)
        b.mystream=self

        """
        if hasattr(b, "next"):
            delattr(b,"next")
        """

        #b.pos = len(self.notes)

        if len(self.notes) > 0:
            b.last = self.notes[-1]
            b.last.next = b

            if b.myoffset >= b.last.myoffset:
                b.pos = len(self.notes)
            else:
                #print "dirty pos stream\n"
                b.pos = len(self.notes)

        else:
            b.pos = len(self.notes)

        self.notes.append(b)
        return b

    def getFirstNoteIndexofChordIndex(self, chordind):
        ret = 0
        for x in xrange(chordind):
            ret = ret + len(self.notes[x])
        return ret


    def decorate(self):
        inhandnotes = self.sort()

        handnotes = MyStream()
        handnotes.song = inhandnotes.song

        for tmp in range(len(inhandnotes.notes)):
            #ntmp = myStream.MyStreamNoteItem(inhandnotes[tmp])
            handnotes.append(inhandnotes.notes[tmp])


        if len(inhandnotes.notes)>1:
            """
            for tmp in range(len(inhandnotes.notes)):
                #ntmp = myStream.MyStreamNoteItem(inhandnotes[tmp])
                handnotes.append(inhandnotes.notes[tmp])
            """



            for tmp in range(len(handnotes.notes)-1):
            #for tmp in range(len(handnotes.notes)):
                # link them
                handnotes.notes[tmp].next=handnotes.notes[tmp+1]
                handnotes.notes[tmp+1].last=handnotes.notes[tmp]


            for x in range(len(handnotes)):
                # pos
                handnotes.notes[x].pos=x

            # chordify
            tmp=handnotes.notes[0]
            start=tmp
            aChord = MyKnownChord()
            aChord.append(start)
            while hasattr(start,"next"):
            #while start.next:
                # oh oh was there was something wrong here
                while hasattr(start,"next") and (start.next.myoffset-start.myoffset) < ischordms:
                #and commented out ..
                #while start.next and (start.next.myoffset-start.myoffset) < ischordms:
                    start.chord=aChord
                    start=start.next
                    aChord.append(start)
                    start.chord = aChord
                if hasattr(start,"next"):
                #if start.next:
                    start.chord = aChord
                    bChord = MyKnownChord()
                    aChord.nextChord=bChord
                    bChord.lastChord=aChord
                    aChord=bChord

                    start=start.next
                    start.chord=aChord
                    aChord.append(start)




        return handnotes


    def __str__(self):
        return str(self.notes)



class MyStreamNoteItem(object):
    def __init__(self, aNote):
        object.__setattr__(self, 'note', aNote)
        #self.note = aNote
        self.mystream=None
        self.pos = None
        #self.next = None
        #self.last = None
        #self.nextChord = None
        #self.lastChord = None
        self.persistentexception.extend(["last","next","lastChord", "nextChord", "mystream"])


    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except:
            return getattr(object.__getattribute__(self,"note"), name)
        pass

    def __str__(self):
        return str(object.__getattribute__(self,"note"))

    def __repr__(self):
        return repr(object.__getattribute__(self,"note"))
        #return str([id(self.mystream), repr(self.note)])


class MyStreamNoteItemFutureProxy(object):
    def __init__(self, astream , apos):
        self.mystream=astream
        self.pos = apos
        print "MyStreamNoteItemFutureProxy usage"
        #self.persistentexception.extend(["last","next","lastChord", "nextChord", "mystream"])


    def __getattribute__(self, name):
        if name == "next":
            try:
                s = object.__getattribute__(self,"mystream")
                p = object.__getattribute__(self,"pos")

                return s[p]
            except:
                return None
        if name == "pos":
            return -1

        return None


    def __str__(self):
        s = object.__getattribute__(self,"mystream")
        p = object.__getattribute__(self,"pos")

        try:
            return "self.next=" + str(s[p])
        except:
            return str(None)
        pass


    def __repr__(self):
        return repr(None)



def create_teststream_wrong_start(midi=60,notes=20):

    s = MyStream()
    a = MyNote()

    #notes = 20
    #midi = 40
    a._midi= 60
    a._myoffset=random.randint(0,1000)
    a._myduration = 100 + random.randint(0,1000)
    a.volume=100
    s.append(a)

    for i in xrange(notes):
        a = MyNote()
        a._midi= midi
        a._myoffset=s[-1].myoffset + random.randint(0,1000)
        a._myduration = 100 + random.randint(0,1000)
        a.volume=100
        s.append(a)

    s.decorate()
    s.toXml2file("midi"+ str(midi)+  ".xml")

def create_teststream_miss(midi=60,notes=20):

    s = MyStream()
    a = MyNote()

    sout = MyStream()

    #notes = 20
    #midi = 40
    a._midi= 60
    a._myoffset=random.randint(0,1000)
    a._myduration = 100 + random.randint(0,1000)
    a.volume=100
    s.append(a)

    b = a.clone()
    sout.append(b)

    for i in xrange(notes):
        a = MyNote()
        a._midi= midi + i
        a._myoffset=s[-1].myoffset + random.randint(0,1000)
        a._myduration = 100 + random.randint(0,1000)
        a.volume=100
        s.append(a)


        #if random.randint(0,10) < 8:
        if not (i == 5):
            b = a.clone()
            sout.append(b)

    s.decorate()
    s.toXml2file("test_kn_miss.xml")

    sout.decorate()
    sout.toXml2file("test_in_miss.xml")




def create_teststream_jump_error(midi=60,notes=20):

    s = MyStream()
    a = MyNote()


    a._midi= midi
    a._myoffset=random.randint(0,1000)
    a._myduration = 100 + random.randint(0,1000)
    a.volume=100
    s.append(a)

    #notes = 20
    #midi = 40

    for i in xrange(notes):
        a = MyNote()
        if i > notes/2:
            a._midi= midi+ notes/2 -i
        else:
            a._midi= midi-i
        a._myoffset=s[-1].myoffset + random.randint(0,1000)
        a._myduration = 100 + random.randint(0,1000)
        a.volume=100
        s.append(a)

    #a = s[notes/2]
    #a.midi= midi +1
    #a._myoffset=random.randint(0,1000)
    #a._myduration = 100 + random.randint(0,1000)
    #a.volume=100

    s.decorate()
    s.toXml2file("jump_error_played"+ str(midi)+  ".xml")

    s = MyStream()
    a = MyNote()

    a._midi= midi
    a._myoffset=random.randint(0,1000)
    a._myduration = 100 + random.randint(0,1000)
    a.volume=100
    s.append(a)

    #notes = 20
    #midi = 40

    for i in xrange(notes):
        a = MyNote()
        if i > notes/2 and False:
            a._midi= midi-1
        else:
            a._midi= midi-i

        a._myoffset=s[-1].myoffset + random.randint(0,1000)
        a._myduration = 100 + random.randint(0,1000)
        a.volume=100
        s.append(a)

    #a = s[notes/2]
    #a._midi= midi +1
    #a._myoffset=random.randint(0,1000)
    #a._myduration = 100 + random.randint(0,1000)
    #a.volume=100

    s.decorate()
    # s.toXml2file("jump_error_known"+ str(midi)+  ".xml")
    return s





if __name__ == '__main__':
    #create_teststream_wrong_start()
    #create_teststream_wrong_start(40)

    s = create_teststream_jump_error(60,10)

    print "s done"
    time.sleep(10)

    print "clearing s"
    s = create_teststream_jump_error(60,10000)
    #s=None
    #print gc.garbage
    time.sleep(10)

    s = 1
    time.sleep(10)



    #create_teststream_miss()

