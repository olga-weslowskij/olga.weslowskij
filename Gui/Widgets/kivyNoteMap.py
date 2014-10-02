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

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton


class KivyNoteMap(GridLayout):


    # reuse
    def config(self, inchord, orgchord=None):
        self.build = False

        self.width=50
        self.height=150
        self.size_hint_y=None

        #self.size_hint_x=None
        #self.cols=1

        self.cols=1

        self.inchord = inchord

        self.knownchord= orgchord


        #self.notesdats = GridLayout(cols=1)
        #self.add_widget(self.notesdats)


        if self.orgchord:
            if orgchord is not None:
                #self.orgchord = ToggleButton(text="("+orgchord.prettyprint()+")")

                self.orgchord.text = "("+orgchord.noteName()+")"
                self.orgchord.kivyNoteMap= self
                self.orgchord.myStreamNote = orgchord
            else:
                self.orgchord.text = "("+str(None)+")"
                self.orgchord.kivyNoteMap= self
                self.orgchord.myStreamNote = None
        else:
            if orgchord is not None:
                #self.orgchord = ToggleButton(text="("+orgchord.prettyprint()+")")
                self.orgchord = ToggleButton(text="("+orgchord.noteName()+")")
                self.orgchord.kivyNoteMap= self
                self.orgchord.myStreamNote = orgchord
            else:
                self.orgchord = ToggleButton(text="("+str(None)+")")
                self.orgchord.kivyNoteMap= self
                self.orgchord.myStreamNote = None



        #btnname= repr(", ".join(map(str,inchord)))
        try:
            #btntxt = inchord.prettyprint()
            btntxt = inchord.noteName()

        except:
            btntxt = "None"

        if self.chord:
            self.chord.text = btntxt
        else:
            self.chord = ToggleButton(text=btntxt)

        # link back for playback
        self.chord.kivyNoteMap= self
        self.chord.myStreamNote = inchord

        #self.progress= ProgressBar(max=1, value=0.5)

        if self.speed:
            self.speed.text="1"
        else:
            self.speed =Label(text="1")


        if self.myoffset:
            if inchord:
                self.myoffset.text=str(inchord.myoffset)
            else:
                self.myoffset.text="-"

        else:
            if inchord:
                self.myoffset = Label(text=str(inchord.myoffset))
            else:
                self.myoffset = Label(text="-")

        # what a name ????
        #self.build = True

        if self.error:
            self.error.text=''
        else:
            self.error = Label(text='')


        if inchord:
            if self.myvolume:
                self.myvolume.text=str(inchord.volume)
            else:
                self.myvolume = Label(text=str(inchord.volume))

            if self.myduration:
                self.myduration.text=str(inchord.myduration)
            else:
                self.myduration = Label(text=str(inchord.myduration))
        else:
            if self.myvolume:
                self.myvolume.text=str(None)
            else:
                self.myvolume = Label(text=str(None))

            if self.myduration:
                self.myduration.text=str(None)
            else:
                self.myduration = Label(text=str(None))


    def build(self, inchord, orgchord=None):
        self.build = False

        self.width=50
        self.height=150
        self.size_hint_y=None

        #self.size_hint_x=None
        #self.cols=1

        self.cols=1

        self.inchord = inchord

        self.knownchord= orgchord


        #self.notesdats = GridLayout(cols=1)
        #self.add_widget(self.notesdats)


        if orgchord is not None:
            #self.orgchord = ToggleButton(text="("+orgchord.prettyprint()+")")
            self.orgchord = ToggleButton(text="("+orgchord.noteName()+")")
            self.orgchord.kivyNoteMap= self
            self.orgchord.myStreamNote = orgchord
        else:
            self.orgchord = ToggleButton(text="("+str(None)+")")
            self.orgchord.kivyNoteMap= self
            self.orgchord.myStreamNote = None


        #btnname= repr(", ".join(map(str,inchord)))
        try:
            #btntxt = inchord.prettyprint()
            btntxt = inchord.noteName()

        except:
            btntxt = "None"
        self.chord = ToggleButton(text=btntxt)

        # link back for playback
        self.chord.kivyNoteMap= self
        self.chord.myStreamNote = inchord

        #self.progress= ProgressBar(max=1, value=0.5)

        self.speed =Label(text="1")
        if inchord:
            self.myoffset = Label(text=str(inchord.myoffset))

        else:
            self.myoffset = Label(text="-")

        # what a name ????
        #self.build = True

        self.error = Label(text='')

        if inchord:
            self.myvolume = Label(text=str(inchord.volume))
            self.myduration = Label(text=str(inchord.myduration))
        else:
            self.myvolume = Label(text=str(None))
            self.myduration = Label(text=str(None))


            #self.add_widget(self.chord)
        #self.add_widget(self.progress)
        #self.add_widget(self.speed)
    """
    def add_widget(self, widget, index=0):
        if self.build:
            if widget is self.speed:
                super(KivyNoteMap,self).add_widget(widget,index)
                if len(widget.text)> 0:
                    #self.width=100
                #self.add_widget(widget,index)
            else:
                self.notesdats.add_widget(widget,index)
        else:
            super(KivyNoteMap,self).add_widget(widget,index)

    """


