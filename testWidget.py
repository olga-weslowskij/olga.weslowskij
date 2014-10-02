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

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from Game.mySong import MySong
from Gui.Widgets.objectWidget import TreeLayout
from libtesting.myscrollview import ScrollView


class a(object):
    def __init__(self):
        self.name="hallo"
        self.adict=[1,2,3,4]
        self.alist={1:1,2:2,3:3,4:4}




class Example1(App):

    def build(self):

        self.widget = Widget()

        self.notesscroller = ScrollView(size_hint=(1,1-0), size=(800,800))

        self.notesscroller.do_scroll_x=True
        self.notesscroller.do_scroll_y=True

        #
        #self.layout.bind(minimum_height=layout.setter('height'))


        #self.layout = RelativeLayout(size=(10000,10000), size_hint=(None,None))
        self.layout = TreeLayout(size=(800,800), size_hint=(None,None))

        #objWidget.add_obj({1: 'Hallo'})

        self.song = MySong()
        song= self.song
        #self.song.fromXml2file("Output.xml")


        adict ={"1":"hallo", "2":"Welt"}

        song.fromXml2file("/home/test/PycharmProjects/olga/Songs/OlgaXml/Chopin284.xml")



        #self.widget.add_widget(self.layout)


        self.graphwidget = self.layout
        self.graphwidget.debug = True
        self.graphwidget.build(self.notesscroller)

        obj=a()
        self.layout.add_obj(obj,deeplevel=1)

        self.notesscroller.add_widget(self.graphwidget)


        #self.layout.bind(minimum_size=self.layout.setter('size'))
        #self.layout.bind(minimum_width=self.layout.setter('width'))

        self.widget.add_widget(self.notesscroller)




        return self.widget

        ti = TextInput(text='Hallo')
        #ti._refresh_text()
        ti._update_graphics()
        return ti
        #return TreeViewButton(text='Hallo')


        """

        carousel = Carousel(direction='right')
        for i in range(10):
            src = "http://placehold.it/480x270.png&text=slide-%d&.png" % i
            image = Factory.AsyncImage(source=src, allow_stretch=True)
            carousel.add_widget(image)
        return carousel
        """









import hotshot
import signal
import code
import traceback

prof = hotshot.Profile("main.prof")


import sys
import readline
readline.parse_and_bind("tab: complete")



def console():
    type, value, tb = sys.exc_info()
    traceback.print_exc()
    last_frame = lambda tb=tb: last_frame(tb.tb_next) if tb.tb_next else tb
    frame = last_frame().tb_frame
    ns = dict(frame.f_globals)
    ns.update(frame.f_locals)
    code.interact(local=ns)


def debug(sig, frame):
    """Interrupt running process, and provide a python prompt for
    interactive debugging."""
    d={'_frame':frame}         # Allow access to frame object.
    d.update(frame.f_globals)  # Unless shadowed by global
    d.update(frame.f_locals)

    i = code.InteractiveConsole(d)
    message  = "Signal recieved : entering python shell.\nTraceback:\n"
    message += ''.join(traceback.format_stack(frame))
    i.interact(message)


def listen():
    signal.signal(signal.SIGUSR1,debug)


def updateGui(dt):
    #()
    #app.layout.move()
    print str(app.song.musicxmlString)
    pass


if __name__ == '__main__':
    try:
        #gc.disable()

        listen()
        Clock.schedule_interval(updateGui, 5.0)
        app= Example1()
        app.run()


    except:
        console()





