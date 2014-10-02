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

from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from Game.gameEngineRoot import GameEngineRoot

from Gui.MyScreenController import ScreenState
from Gui.Screens.myScreen import MyScreen
from Gui.Widgets.infoLogWidget import InfoLogWidget
import myglobals
from Game.options import optionswidgets, RecommendOptionsValues
#import pianoSimonGame
import json


class labeledWidget(BoxLayout):

    #def __init__(self):
        #self.build()
     #   pass

    def build(self, awidget):
        self.orientation = 'horizontal'
        self.label = Label()
        self.add_widget(self.label)
        self.widget = awidget
        self.add_widget(self.widget)




def buildLabeledTextWidget(text = "fill me", aWidget=None):
    client = labeledWidget()
    client.build(TextInput(multiline=False))
    client.label.text= text
    return client


def buildOptionWidget(name):
    client = labeledWidget()
    spinner = Spinner(text=RecommendOptionsValues[name].keys()[0], values = RecommendOptionsValues[name].keys())
    client.build(spinner)
    client.label.text= name
    optionswidgets[name] = spinner
    return client




class MidiConfigScreen(MyScreen):

    def __init__(self,**kwargs):
        super(MidiConfigScreen, self).__init__(**kwargs)

        self.initdone=False

        self.options={}

        self.options["midi in"] = "midi in"
        self.options["midi out"] = "midi out"
        self.options["midi.volume"] = "midi.volume"
        self.options["update Gui"] = "update Gui"

        self.mystate="MidiConfig"

    def build(self):
        self.initdone=True
        # only too build MdidController and fill options midi in and midi out
        #myglobals.gameState = pianoSimonGame.PianoSimonGame()
        #myglobals.gameState = gameEngineRoot.PianoSimonGame2()
        #myglobals.gameState.myMidiController = MyMidiController()

        self.widget = BoxLayout(orientation='vertical')

        #self.fileChooser = FileChooserListView()

        #self.widget.add_widget(self.fileChooser)


        #self.widget.add_widget(buildLabeledTextWidget(text="client"))
        #self.widget.add_widget(buildLabeledTextWidget(text="port"))
        #self.widget.add_widget(buildLabeledTextWidget(text="Song"))
        for x in RecommendOptionsValues.keys():
            if self.options.get(x,None) is not None:
                self.widget.add_widget(buildOptionWidget(x))

        #optionswidgets["speedtol"].text='easy'
        #optionswidgets["hand"].text='left and right'

        self.loadOptions()

        #self.widget.add_widget(buildLabeledTextWidget(text="Hand"))

        #self.widget.add_widget(buildLabeledTextWidget(text="Timing"))


        def callback(instance):
            if myglobals.gameState:
                myglobals.gameState.initdone=False
            self.saveOptions()
            try:
                myglobals.gameState.myMidiController.build()
                ScreenState.change_state("OlgasDuty")
                #ScreenState.change_state("OlgaDocuScreen")
            except:
                instance.text= "select a connected midi device please."
                pass

        btn = Button(text='OlgasDuty')
        btn.bind(on_press=callback)
        self.widget.add_widget(btn)

        """
        self.logWidget = InfoLogWidget()
        self.logWidget.build()
        self.logWidget.size_hint=(1,1)
        self.widget.add_widget(self.logWidget)
        """


        #self.mystate=astateName

        ScreenState.add_state(self)

        return self.widget

    def on_enter(self, tostate):
        if not(self.initdone):
            self.build()
        super(MidiConfigScreen,self).on_enter(tostate)


    def on_leave(self, tostate):

        super(MidiConfigScreen,self).on_leave(tostate)


        # redo init
        if myglobals.gameState:
            myglobals.gameState.initdone=False
        else:
            #myglobals.gameState = pianoSimonGame.PianoSimonGame()
            myglobals.gameState = GameEngineRoot()

    def update(self):
        pass
        #if optionswidgets["speedtol"].text == "normal":
        #    ScreenState.change_state("Played")

    def loadOptions(self):
        with open('midiconfig.json', 'rb') as fp:
            allOptions = json.load(fp)

        for x in allOptions.keys():
            print "midiConfigScreen loading " + str(x)
            #pdb.set_trace()

            if self.options.get(x,None) is not None:
                optionswidgets[x].text=str(allOptions[x])

    def saveOptions(self):
        allOptions = {}
        for x in self.options.keys():
            allOptions[x]=optionswidgets[x].text

            with open('midiconfig.json', 'wb') as fp:
                json.dump(allOptions, fp)

