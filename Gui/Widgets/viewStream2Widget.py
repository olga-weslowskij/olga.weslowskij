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
from kivy.adapters.simplelistadapter import SimpleListAdapter
from kivy.uix.gridlayout import GridLayout
from Gui.Screens.aViewNotesScreen import SelectNotes
from Gui.Widgets.kivyNoteMap import KivyNoteMap
from Gui.Widgets.listview8 import ListView8
from mylibs.myDict import MyDict

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)



class ViewStream2Adapter(SelectNotes, SimpleListAdapter):

    def __init__(self):
        self.song= None
        self.stream=None
        self.build()
        self.data = []

    def build(self):
        SelectNotes.build(self)
        self.widget = GridLayout(cols=10, size_hint_y=None)
        self.widget.bind(minimum_height=self.widget.setter('height'))
        return self.widget

    def updateGui(self):
        print "update" + self.__class__.__name__

    def clear(self, children):
        pass

    def get_view(self, index):
        if len (self.data) == 0:
            return None

        if index >= len(self.data):
            return None
        #return self.buildkivyMelodyRating(index)

        #print self.stream[-1].prettyprint()
        return self.data[index]


    def set_view(self,index, item):
        while index >= len(self.data):
            self.data.append(None)

        self.data[index] = item



class ViewStream2Widget(ListView8,object):
    def __init__(self, *args, **kwargs):
        super(ViewStream2Widget,self).__init__(*args, **kwargs)
        self.reinit()

    def reinit(self):
        self.donelen = 0
        self.shownMelodyRun=None
        self.shownKivyNoteMap=[]
        self.shownMelodyRating=MyDict()
        self.shownMelodyRating.defaultNone=True

        self.shownpos ={}
        self.shownpos[0]=0
        self.shownpos[1]=0

        self.widget = self

        self.adapter = ViewStream2Adapter()

        self.do_scroll_x=True
        self.do_scroll_y=True

        self.toshow = None


    @property
    def run(self):
        return self.toshow


    @run.setter
    def run(self, value):
        if self.toshow == value:
            self.toshow = value
        else:
            self.reinit()
            self.toshow = value



    """
    def updateGui(self):
        self.adapter.updateGui()
        self._trigger_reset_populate()
    """

    def play(self):
        self.adapter.play()

    def updateGui(self):
        """if not(self.shownMelodyRun is None or self.shownMelodyRun != self.toshow):
            return
            """

        toshow = self.toshow

        index = len(self.shownKivyNoteMap)

        if toshow is None:
            print "Show Stream2 None"
            for i in xrange(index):
                self.shownKivyNoteMap[i] = None
                self.adapter.set_view(self.shownpos[i], None)
            self._trigger_reset_populate()
            return

        # belongs in update, but i dont have update widget ..
        # check needs improvemnt in mystream
        # ( Mystream will be a tree someday, far far far in the future... and log changes)

        """
        if self.shownMelodyRun == self.toshow and len(self.shownMelodyRun) == len(self.toshow):
            print "nothing to update"
            return
        # rest belong in updateGui
        """



       # print self.toshow.prettyprint()

        newlen = len(toshow.notes)



        #for x in self.notesscroller.stream:


        news = False
        # extend

        while ( len(self.shownKivyNoteMap)< newlen):
            self.shownKivyNoteMap.append(None)
            news = True

        """
        what is with changed???
        changes can be duration, other stream..
        if news == False:
            return
        """

        #update all changed
        # starting from back
        start = 0
        for start in xrange(newlen-1, -1,-1):
            news = True
            if toshow.notes[start] == self.shownMelodyRating[start]:
                start = start+1
                #pass
                break

        print "updating " + str([start,newlen])
        #logger.info("updating " + str([start+1,newlen]))

        #for i in xrange(start+1, newlen):
        for i in xrange(start, newlen):
        #for i in xrange(newlen):
            if toshow.notes[i] != self.shownMelodyRating[i] or True:
                #if self.shownKivyNoteMap[i]:
                #    self.notesscroller.widget.remove_widget(self.shownKivyNoteMap[i])
                #    self.notesscroller.widget.remove_widget(self.shownKivyNoteMap[i].speed)
                self.shownKivyNoteMap[i] = self.buildKivyNoteMap(toshow,i)

                if len(self.shownKivyNoteMap[i]) == 2:
                    self.shownpos[i+1]= self.shownpos[i] + 2
                    self.adapter.set_view(self.shownpos[i]+1, self.shownKivyNoteMap[i][0])
                    self.adapter.set_view(self.shownpos[i], self.shownKivyNoteMap[i][1])
                else:
                    self.shownpos[i+1]= self.shownpos[i] + 1
                    self.adapter.set_view(self.shownpos[i], self.shownKivyNoteMap[i][0])
                    #self.notesscroller.data[self.shownpos[i]] = self.shownKivyNoteMap[i][0]

                self.shownMelodyRating[i] = toshow.notes[i]

        #logger.info("clearing " + str([newlen,len(self.shownKivyNoteMap)]))

        for i in xrange(newlen, len(self.shownKivyNoteMap)):
            self.shownKivyNoteMap[i] = None
            self.shownMelodyRating[i] = None
            self.adapter.set_view(self.shownpos[i], None)

        self.donelen = index
        #len(self.notesscroller.stream)

        #self.notesscroller.updateGui()

        if (news):
            #self.notesscroller.data = self.shownKivyNoteMap
            self._trigger_reset_populate()

        self.shownMelodyRun = toshow
        pass

    def buildKivyNoteMapSimple(self, toshow, i, notesandrightspeed = None):

        x = toshow.notes[i]

        btn = KivyNoteMap()


        btn.build(x)

        #btn.chord.playstream = self.stream

        btn.add_widget(btn.chord)
        btn.chord.bind(on_press=self.adapter.selectBtn)

        btn.add_widget(btn.myoffset)

        #self.widget.add_widget(btn)

        return [btn]



    def buildKivyNoteMap(self, toshow, i, notesandrightspeed = None):

        x = toshow.notes[i]

        btn = KivyNoteMap()

        #btn.build(toshow.notes[i].getInNote(), toshow.notes[i].getKnownNote())
        btn.build(toshow.notes[i],None)

        """
        if type(x) is list:
            btn.build(x)
        else:
            btn.build([x])
        """

        #btn.progress.value=1
        #btn.speed.text=str(x)
        #btn.add_widget(btn.orgchord)
        #btn.orgchord.bind(on_press=self.notesscroller.selectBtn)
        btn.add_widget(btn.chord)
        btn.chord.bind(on_press=self.adapter.selectBtn)

        btn.add_widget(btn.myoffset)

        #btn.add_widget(Label(text="id:" + str(id(x))))
        #btn.myduration.text="id:" + str(id(x))

        btn.add_widget(btn.myduration)

        """
        if toshow.notes[i].getKnownNote():
            btn.myvolume.text=str(toshow.notes[i].getKnownNote().myoffset)
        else:
            btn.myvolume.text="None"

        btn.add_widget(btn.myvolume)
        """

        #if x.getCurrent2RunSpeed():
        spacingtime = False
        if hasattr(toshow[i],"chord"):
            spacingtime = i > 0 and toshow[i].chord.pos != toshow[i-1].chord.pos
        if spacingtime:

            text = ""
            btn.speed.text= text
            btn.speed.halign="right"
            #btn.add_widget(btn.speed)


        #if x.getCurrent2RunSpeed():
            #self.notesscroller.data.append(btn.speed)
            #self.notesscroller.widget.add_widget(btn.speed)

        # examine layoutbug
        #spacingtime = False

        if spacingtime:
            #self.notesscroller.data.append(btn.speed)
            #self.notesscroller.widget.add_widget(btn.speed)
            btn.speed.height = btn.height
            btn.speed.size_hint_y=None
            return [btn, btn.speed]
            #btn.add_widget(btn.speed)

        #self.notesscroller.data.append(btn)
        #self.notesscroller.widget.add_widget(btn)

        return [btn]

