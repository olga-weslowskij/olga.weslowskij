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

from Gui.Screens.myScreen import MyScreen
from Gui.Widgets.objectWidget import TreeLayout
from libtesting.myscrollview import ScrollView

# TODO this is inverted
from myglobals import ScreenState
import myglobals


class ConfigObjectScreen(MyScreen):
    def __init__(self):
        super(ConfigObjectScreen,self).__init__()
        self._object=None
        self.btnbar=None
        self.debug = True

    def on_enter(self, tostate):
        super(ConfigObjectScreen, self).on_enter(tostate)
        #SimonRequests.createShowErrorStream(myglobals.SimonMode.activeChallenge().challenge)

        print self.mystate

        if self.object:
            self.update()


    def on_leave(self, tostate):
        super(ConfigObjectScreen,self).on_leave(tostate)
        # reanbled
        #self.notesscroller.remove_widget(self.layout)
        pass


    def updateGui(self):
        pass


    @property
    def object(self):
        return self._object


    @object.setter
    def object(self, value):
        if value != self._object:
            self._object=value
            try:
                self.notesscroller.remove_widget(self.layout)
                self.update()
            except:
                pass

        return


    def update(self):
        if self.object and len(self.notesscroller.children)==0:
            #
            #self.layout.bind(minimum_height=layout.setter('height'))


            #self.layout = RelativeLayout(size=(10000,10000), size_hint=(None,None))
            self.layout = TreeLayout(size=(800,800), size_hint=(None,None))


            #objWidget.add_obj({1: 'Hallo'})

            self.layout.build(self.notesscroller)
            print "building OBJECT " + str(self.object)
            self.layout.debug = self.debug
            self.layout.add_obj(self.object, deeplevel=1)

            self.notesscroller.add_widget(self.layout)


            #self.layout.bind(minimum_size=self.layout.setter('size'))
            #self.layout.bind(minimum_width=self.layout.setter('width'))

            #self.widget.add_widget(self.notesscroller)

    def build(self):
        self.widget= BoxLayout(orientation='vertical')

        self.notesscroller = ScrollView(size_hint=(1,1-0), size=(1600,800))
        self.notesscroller.do_scroll_x=True
        self.notesscroller.do_scroll_y=True


        self.widget.add_widget(self.notesscroller)


        if self.btnbar is None:
            self.btnbar=GridLayout(cols=7, size_hint=(1,0.2))

        self.widget.add_widget(self.btnbar)


        def callbackplay70(instance):
            #main.console()
            myglobals.gameState.console = True

        btn70 = Button(text='Console')

        btn70.bind(on_press=callbackplay70)
        self. btnbar.add_widget(btn70)

        def callback(instance):
            self.notesscroller.remove_widget(self.layout)
            #self.layout.move()
            #self.update()


        btnRoot = Button(text='root')
        btnRoot.bind(on_press=callback)
        self.btnbar.add_widget(btnRoot)



        def callback(instance):
            self.debug= not(self.debug)
            instance.text ="debug=" + str(self.debug)
            #self.notesscroller.remove_widget(self.layout)
            self.layout.debug = self.debug
            self.layout.move()
            #self.update()


        btndebug = Button(text='toggle debug')
        btndebug.text ="debug=" + str(self.debug)
        btndebug.bind(on_press=callback)
        self.btnbar.add_widget(btndebug)



        def callback(instance):
            myglobals.ScreenState.change_state_back()

        btn = Button(text='Back')
        btn.bind(on_press=callback)
        self.btnbar.add_widget(btn)


        def changeStateCallback(instance):
            myglobals.ScreenState.change_state(instance.mystate)

        btnOlgasDuty = Button(text='OlgasDuty')
        btnOlgasDuty.mystate = "OlgasDuty"
        btnOlgasDuty.bind(on_press=changeStateCallback)
        self.btnbar.add_widget(btnOlgasDuty)



        myglobals.ScreenState.add_state(self)







