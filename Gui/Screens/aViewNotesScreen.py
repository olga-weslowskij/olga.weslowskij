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

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from Game import options
from Game.myLogHandler import infoLog
from Gui.MyScreenController import ScreenState

from Gui.Screens.myScreen import MyScreen

#from pianosimon import updateGame
#from Gui.Widgets.kivyNoteMap import KivyNoteMap
from Gui.Widgets.infoLogWidget import InfoLogWidget
from Gui.Widgets.kivyNoteMap import KivyNoteMap
import myglobals

import logging
logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ +  '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)


class SelectNotes(object):
    def build(self):
        self._selectedBtn=[]
        self.maxselectzed = 2
        self.stream= None
        self.speed=1.0

    def selectBtn(self, instance):
        #print "Button Selected 1 " + str(instance) +" " + str(instance.state)
        self._selectedBtn.append(instance)
        #instance.state = 'down'
        while len(self._selectedBtn) > self.maxselectzed:
            tmp = self._selectedBtn.pop(0)
            tmp.state='normal'

        for x in self._selectedBtn:
            x.state='down'

        #print "Button Selected 2" + str(self._selectedBtn)
        #print "Button Selected 2" + str(instance) +" " + str(instance.playstream)


    def play(self):
        stream1= self.getStream()
        if stream1 is None:
            return
        #print "SelectNotes playing " + str(stream1) + " " + str([indx,endx])
        #print "playing at speed: " + str(self.speed)
        self.output = myglobals.gameState.myMidiController.getMidiOut()
        if type(stream1[0]) is list:
            self.output.playpartMyStream(stream1 , 0 , len(stream1), startchord=stream1[0],speed=self.speed)
        else:
            self.output.playpartMyStream(stream1 , 0 , len(stream1), startnote=stream1[0],speed=self.speed)




    def getStream(self):
        if len(self._selectedBtn) <2:
            if self.stream:
                indx = 0
                endx = len(self.stream)
                stream = self.stream
            else:
                print "SelectNotes no Stream"
                return
        else:
            # play hole chords only

            stream1 = self._selectedBtn[0].myStreamNote.mystream
            stream2 = self._selectedBtn[1].myStreamNote.mystream


            start = self._selectedBtn[0].myStreamNote
            end = self._selectedBtn[1].myStreamNote

            if start.myoffset > end.myoffset:
                start = self._selectedBtn[1].myStreamNote
                end = self._selectedBtn[0].myStreamNote


            #stream = self._selectedBtn[0].KivyNoteMap.noterating.map.inwort

            # no mixing TODO
            if stream1 != stream2:
                print "SelectNotes different Streams"
                return None

        return stream1.buildAllInChordRange(start, end)


    def getList(self):
        if len(self._selectedBtn) <2:
            if self.stream:
                indx = 0
                endx = len(self.stream)
                stream = self.stream
            else:
                print "SelectNotes no Stream"
                return
        else:
            # play hole chords only

            stream1 = self._selectedBtn[0].myStreamNote.mystream
            stream2 = self._selectedBtn[1].myStreamNote.mystream


            start = self._selectedBtn[0].myStreamNote
            end = self._selectedBtn[1].myStreamNote

            if start.myoffset > end.myoffset:
                start = self._selectedBtn[1].myStreamNote
                end = self._selectedBtn[0].myStreamNote


            #stream = self._selectedBtn[0].KivyNoteMap.noterating.map.inwort

            # no mixing TODO
            if stream1 != stream2:
                print "SelectNotes different Streams"
                return None

        return stream1.buildAllInChordRangeList(start, end)







class AViewNotesScreen(MyScreen):

    def __init__(self):
        super(AViewNotesScreen,self).__init__()
        self.btnbar = None
        self.notesscroller=None


    def buildbtnbar(self):
        if self.btnbar is None:
            self.btnbar=GridLayout(cols=7, size_hint=(1,0.2))

        btnbar = self.btnbar

        def changeStateCallback(instance):
            myglobals.ScreenState.change_state(instance.mystate)


        def callbackplay70(instance):
            #main.console()
            myglobals.gameState.console = True


        btn70 = Button(text='Console')

        btn70.bind(on_press=callbackplay70)
        btnbar.add_widget(btn70)

        def callbackplay80(instance):
            #main.console()
            myglobals.gameState.test()

        btn80 = Button(text='test')

        btn80.bind(on_press=callbackplay80)
        btnbar.add_widget(btn80)


        def callback14(instance):
            ScreenState.mystate.dirty = True
            ScreenState.updateGui()


        btn14 = Button(text='update\nGui')
        btn14.bind(on_press=callback14)
        btnbar.add_widget(btn14)


        def callbackplay(instance):
            #print "replaying " + str(self.notesscroller._selectedBtn[0]) + " " + str(self.notesscroller._selectedBtn[1])
            self.notesscroller.play()

        btn4 = Button(text='Play\nselected\nChords')
        btn4.speed = 1.0
        btn4.bind(on_press=callbackplay)
        btnbar.add_widget(btn4)


        def callback(instance):
            ScreenState.change_state_back()

        btn = Button(text='Back')
        btn.bind(on_press=callback)
        btnbar.add_widget(btn)


        btnOlgasDuty = Button(text='OlgasDuty')
        btnOlgasDuty.mystate = "OlgasDuty"
        btnOlgasDuty.bind(on_press=changeStateCallback)
        btnbar.add_widget(btnOlgasDuty)

        return btnbar

    def build(self):
        #self.btnbar=GridLayout(cols=7, size_hint=(1,0.2))
        if not hasattr(self,"btnbar"):
            self.btnbar=None

        if self.btnbar is None:
            self.btnbar = self.buildbtnbar()

        print self.btnbar

        self.widget = BoxLayout(orientation='vertical')

        #l = Label(text=str(self.mystate))


        self.logWidget = InfoLogWidget()
        self.logWidget.build()
        self.widget.add_widget(self.logWidget)

        """
        self.logWidget = Label(size_hint=(1,0.1))
        self.widget.add_widget(self.logWidget)
        self.logWidget.text = "hallo"
        infoLog.handlers.append(self.logWidget)
        """


        if not(hasattr(self,"notesscroller")):
            self.notesscroller = ScrollView(size_hint=(1,1-self.btnbar.size_hint_y))

        if self.notesscroller is None:
            print str(self.mystate) + "self.notesscroller is None"
            self.notesscroller = ScrollView(size_hint=(1,1-self.btnbar.size_hint_y))

        #self.notesscroller = ListView8(size_hint=(1,1-self.btnbar.size_hint_y))

        #self.notesscroller = ListView8(size_hint=(1,1-self.btnbar.size_hint_y))


        self.notesscroller.do_scroll_x=True
        self.notesscroller.do_scroll_y=True
        self.widget.add_widget(self.notesscroller)

        #self.notesscroller = anotesscroller
        #self.notesscroller.add_widget(self.notesscroller.widget)



        self.widget.add_widget(self.btnbar)

        l = Label(text=str(self.mystate),size_hint=(1,0.1))
        self.widget.add_widget(l)


        self.dirty=True

        ScreenState.add_state(self)


    def buildAll(self, astateName, anotesscroller):

        self.mystate = astateName
        self.notesscroller=anotesscroller
        self.notesscroller = anotesscroller


        self.widget = BoxLayout(orientation='vertical')


        self.logWidget = InfoLogWidget()
        self.logWidget.build()
        self.widget.add_widget(self.logWidget)

        """
        self.logWidget = Label(size_hint=(1,0.1))
        self.widget.add_widget(self.logWidget)
        infoLog.handlers.append(self.logWidget)
        """

        """
        self.notesscroller = ScrollView(size_hint=(1,0.8))

        self.notesscroller.do_scroll_x=True
        self.notesscroller.do_scroll_y=True
        self.widget.add_widget(self.notesscroller)

        self.notesscroller = anotesscroller
        self.notesscroller.add_widget(self.notesscroller.widget)
        """


        self.widget.add_widget(self.notesscroller)

        self.mystate=astateName

        l = Label(text=str(self.mystate),size_hint=(1,0.1))



        ScreenState.add_state(self)

        #btnbar=GridLayout(cols=8, size_hint=(1,0.2))
        #btnbar=GridLayout(cols=7, size_hint=(1,0.2))
        self.btnbar = self.buildbtnbar()
        self.widget.add_widget(self.btnbar)

        self.widget.add_widget(l)

        return self.widget

    def updateGui(self):
        if self.mystate == "LastError":
            #ShowErrors.computeBestInputMap(5)
            pass
        self.notesscroller.updateGui()


    def update(self):
        #self.notesscroller.update()
        # TODODone dont belong here (All Game states are Screens?)
        # Done but some Screens needed State updates
        #if myglobals.gameState:

        if self.dirty:
            #logger.info("update game")
            #myglobals.gameState.updateGame(0)
            #logger.info("update game done")
            #logger.info("update screen")
            if options.getOptionValue("update Gui"):
                ScreenState.updateGui()
            #logger.info("update screen done")
        #else:
            #myglobals.gameState = pianoSimonGame.PianoSimonGame()

        # pianosimon.updateGame(0)
        pass

