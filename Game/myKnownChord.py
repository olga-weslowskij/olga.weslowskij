
# stolen from myKnownNotes fix imports
#from myStream import MyStream


def note2repr(tmp):
    return tmp.midi


class MyKnownChord(object):

    def __init__(self):
        self.nextChord=None
        self.lastChord=None
        #self.notes=MyStream()
        self.notes=[]

    def append(self,aNote):
        self.notes.append(aNote)

    @property
    def pos(self):
        if len(self.notes)>0:
            return self.notes[0].pos
        return None


    @property
    def myoffset(self):
        if len(self.notes)>0:
            return self.notes[0].myoffset
        return None


    def getChordtonesofType(self,T):
        ret = []
        for x in self.notes:
            if note2repr(x) == note2repr(T):
                ret.append(x)
        return ret

    def __getitem__(self, item):
        return self.notes[item]

    def __len__(self):
        return self.notes.__len__()

    def __iter__(self):
        return self.notes.__iter__()

    def prettyprint(self):
        ret = []
        for x in self.notes:
            ret.append(x.prettyprint())
        return str(ret)

    def __str__(self):
        return str(self.notes)

    def __repr__(self):
        return str(self)


class TheUnknownChord(MyKnownChord):
    def prettyprint(self):
        return "TheUnknownChord"

    def __str__(self):
        return self.prettyprint()


theUnknownChord=TheUnknownChord()
