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
from Gui.Screens.simonGameScreen import SimonGameScreen
from Gui.Widgets.viwRunWidgetVP import ViewRunWidgetVP, ScrollViewUpdate
from Requests import SimonRequests
from libtesting.myscrollview import ScrollView


class SimonViewErrorScreen(SimonGameScreen):
    def __init__(self):
        super(SimonViewErrorScreen,self).__init__()
        self.mystate = "SimonViewErrorScreen"
        self.pianoSimonGame=None

    """
    def on_enter(self, tostate):
        super(SimonViewErrorScreen, self).on_enter(tostate)

        #SimonRequests.createShowErrorStream()

        #self.notesscroller.run =

        print "SimonViewErrorScreen"
    """


    def update(self):
        #SimonRequests.createShowBestActiveStream(None)
        SimonRequests.createShowErrorStream()


    def buildAll(self, astateName, anotesscroller):
        super(SimonViewErrorScreen,self).buildAll(astateName,anotesscroller)
        return
        # new fault widget
        self.notesscroller = ScrollViewUpdate(size_hint=(1,1))


        super(SimonViewErrorScreen,self).buildAll(astateName,self.notesscroller)

        self.notesscroller.do_scroll_x=True
        self.notesscroller.do_scroll_y=True

        self.layout = ViewRunWidgetVP()


        self.layout.build(self.notesscroller)

        self.notesscroller.add_widget(self.layout)




    def updateGui(self):
        #print "updating " + str(self.mystate)
        #SimonRequests.createShowErrorStream(myglobals.SimonMode.activeChallenge().challenge)

        super(SimonViewErrorScreen,self).updateGui()

        pass

    """
    def build(self):
        pass

    """





