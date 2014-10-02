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
from kivy.uix.togglebutton import ToggleButton
from Gui.Widgets.kivyNoteMap import KivyNoteMap
from Gui.Widgets.viewStream2Widget import ViewStream2Widget

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)



class ViewSongWidget(ViewStream2Widget):

    def __init__(self):
        super(ViewSongWidget,self).__init__()
        self.levelstarts = {}
        self.levelends = {}
        self.hands = {}
        self.song = None

    def buildKivyNoteMap(self, toshow, i, notesandrightspeed = None):

        """
        levelstarts = toshow.song.startparts
        levelends = toshow.song.endparts
        hands = toshow.song.handparts
        """



        x = toshow.notes[i]

        btn = KivyNoteMap()


        btn.build(x)

        #btn.chord.playstream = self.stream

        btn.add_widget(btn.chord)
        btn.chord.bind(on_press=self.adapter.selectBtn)

        #btn.add_widget(btn.myduration)
        #btn.add_widget(btn.myvolume)


        tmp = ToggleButton(text = "levelstart" )
        if btn.inchord.pos in self.song.startparts:
            tmp.state = 'down'

        self.levelstarts[btn.inchord.pos] = tmp
        btn.add_widget(tmp)
        #self.endparts=[]
        tmp = ToggleButton(text = "levelend" )
        if btn.inchord.pos in self.song.endparts:
            tmp.state = 'down'
        self.levelends[btn.inchord.pos] = tmp
        btn.add_widget(tmp)

        """
        tmp = Spinner(text="hand", values = map(str,self.song.handparts))
        #tmp = ToggleButton(text = "levelend" )
        tmp.text = str(btn.inchord.hand)
        self.hands[btn.inchord.pos] = tmp
        btn.add_widget(tmp)
        """


        btn.add_widget(btn.myoffset)

        #self.widget.add_widget(btn)

        return [btn]
