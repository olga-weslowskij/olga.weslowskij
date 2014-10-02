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
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from Gui.Screens.aViewNotesScreen import AViewNotesScreen
from myglobals import ScreenState
from Gui.Widgets.viewRunWidget import ViewRunWidget
import myglobals

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)


class ViewARunScreen(AViewNotesScreen):
    def __init__(self):
        super(ViewARunScreen,self).__init__()

    def build(self):
        #self.mystate = self.__class__.__name__
        print "building " + str (self.mystate)
        self.widget = BoxLayout(orientation='vertical')


        self.btnbar=None
        if not hasattr(self,"btnbar"):
            self.btnbar=None

        if self.btnbar is None:
            print "building btnbar"
            self.btnbar = self.buildbtnbar()


        self.notesscroller = ViewRunWidget()

        #self.notesscroller.add_widget(self.notesscroller.widget)

        self.notesscroller.do_scroll_x=True
        self.notesscroller.do_scroll_y=True
        self.widget.add_widget(self.notesscroller)

        #self.notesscroller = anotesscroller
        #self.notesscroller.add_widget(self.notesscroller.widget)

        self.widget.add_widget(self.btnbar)

        ScreenState.add_state(self)

        #btnbar=GridLayout(cols=8, size_hint=(1,0.2))
        #btnbar=GridLayout(cols=7, size_hint=(1,0.2))
        #btnbar = self.buildbtnbar()
        #self.widget.add_widget(btnbar)

    def buildAll(self, astateName, anotesscroller):
        #super(ViewARunScreen,self).buildAll(astateName, ViewRunWidget())
        self.mystate = astateName
        self.build()




    def on_enter(self, tostate):
        super(ViewARunScreen, self).on_enter(tostate)
        #SimonRequests.createShowErrorStream(myglobals.SimonMode.activeChallenge().challenge)



    def updateGui(self):
        if self.notesscroller.run:
            self.notesscroller.updateGui()



    def buildbtnbar(self):
        btnbar=GridLayout(cols=7, size_hint=(1,0.2))

        def changeStateCallback(instance):
            ScreenState.change_state(instance.mystate)


        def callbackplay70(instance):
            #main.console()
            myglobals.gameState.console = True



        btn70 = Button(text='Console')

        btn70.bind(on_press=callbackplay70)
        btnbar.add_widget(btn70)



        """
        def callbackplay8(instance):
            OlgaRequests.playChallenge()
            #ScreenState["Song"].challenge.replay()

        btn8 = Button(text='Play\nChallenge again')
        btn8.speed = 1.0
        btn8.bind(on_press=callbackplay8)
        btnbar.add_widget(btn8)
        """


        def callback14(instance):
            ScreenState.mystate.dirty = True
            ScreenState.updateGui()


        btn14 = Button(text='update\nGui')
        btn14.bind(on_press=callback14)
        btnbar.add_widget(btn14)



        def callbackplay(instance):
            #print "replaying " + str(self.notesscroller._selectedBtn[0]) + " " + str(self.notesscroller._selectedBtn[1])
            self.notesscroller.adapter.play()
            # play and save
            s = self.notesscroller.adapter.getStream()
            s.toXml2file("play.xml")

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






