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

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)


class ViewStreamWidget(ListView8) :
    def __init__(self, *args, **kwargs):
        super(ViewStreamWidget,self).__init__(*args, **kwargs)
        #self.notesscroller = ListView8(size_hint=(1,1-self.btnbar.size_hint_y))
        self.adapter = ViewStreamAdapter()
        self.widget = self

    @property
    def stream(self):
        return self.adapter.stream


    @stream.setter
    def stream(self, value):
        self.adapter.stream = value

    @property
    def toshow(self):
        return self.adapter.stream

    @toshow.setter
    def toshow(self, value):
        self.adapter.stream = value




    def play(self):
        self.adapter.play()


    def updateGui(self):
        self.adapter.updateGui()
        self._trigger_reset_populate()




class ViewStreamAdapter(SelectNotes, SimpleListAdapter):

    def __init__(self):
        self.stream=None
        self.build()

    def build(self):
        SelectNotes.build(self)
        self.widget = GridLayout(cols=10, size_hint_y=None)
        self.widget.bind(minimum_height=self.widget.setter('height'))
        return self.widget

    def clear(self, children):
        pass

    def updateGui(self):
        #print "update ViewStreamAdapter\n"
        if not self.stream:
            return

        print str(self.stream)
        self.widget.clear_widgets()

        #self.notesscrollerTiming = GridLayout(cols=4, size_hint_y=None)
        #self.notesscrollerTiming.bind(minimum_height=self.notesscrollerTiming.setter('height'))
        #self.notesscroller.add_widget(self.notesscrollerTiming)
        index = 0


        data=[]

        print "building kivyNoteMaps " + str(len(self.stream))

        for x in self.stream:
            btn = self.buildkivyMelodyRating(x)
            data.append(btn)
            index +=1
            print str(index) + " ",

        print "building kivyNoteMaps done"
        self.data = data


    def buildkivyMelodyRating(self, x):

        btn = KivyNoteMap()
        btn.build(x)
        btn.progress.value=1
        btn.speed.text=str(x)
        btn.add_widget(btn.chord)
        btn.chord.bind(on_press=self.selectBtn)

        btn.add_widget(btn.myoffset)
        btn.add_widget(btn.myduration)
        btn.add_widget(btn.myvolume)

        #self.widget.add_widget(btn)
        #data.append(btn)



        return btn


    def get_view(self, index):
        if len (self.data) == 0:
            return None

        if index >= len(self.data):
            return None
        #return self.buildkivyMelodyRating(index)

        #print self.stream[-1].prettyprint()
        return self.data[index]