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

#!/usr/bin/env python
import code
import logging

from Game import options
#from Game.chordReport import ChordReport
from Game.myLogHandler import infoLog
from Game.olgaMode import OlgaMode
from Game.simonMode import SimonMode
from myglobals import ScreenState
from Requests.DontAnnoyMeFeedback import DontAnnoyMeFeedback
from Game.historyMode import HistoryMode
from Game.myMidiController import MyMidiController
from Game.myNote import MyNote
from Game.mySong import MySong
from Game.myStream import MyStream
import myglobals

logger = logging.getLogger('pianosimon2')
hdlr = logging.FileHandler('./pianosimon2.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)


class GameEngineRoot(object):

    def __init__(self):
        self.initdone = False
        self.myMidiController = None
        self.console = False
        self.song = None
        myglobals.gameState=self



    def getMidiTick(self):
        if self.myMidiController:
            return self.myMidiController.getMidiTick()
        return None



    #if __name__ == "__main__":
    def initGame(self):


        #global self.analyseplay, ScreenState["Song"].challenge, self.allmymaps, self.bestmap, self.bestactive, self.perfect, newScreenState["Song"].challenge,\
        #self.output, self.output2, self.first , self.initdone, self.input, self.textGui, self.badmelodie, self.goodmelodie, self.thescorefile


        if self.myMidiController is None:
            self.myMidiController = MyMidiController()


        self.scorefile= options.thescorefile

        #if self.input is None and
        self.input= self.myMidiController.getMidiIn()



        if myglobals.HistoryMode is None:
            self.historyMode = HistoryMode()
            self.input.listener.append(self.historyMode)

        # convert
        #asong = MySong()
        #asong.frommusic21(self.scorefile)

        #asong.toXml2file(self.scorefile+".xml")


        #self.SimonMode.song.fromXml2file("Output.xml")

        #code.interact(local=locals())

        if myglobals.SimonMode is None:
            self.SimonMode = SimonMode()
            self.input.listener.append(self.SimonMode)


        if myglobals.OlgaMode is None:
            self.olgaMode = OlgaMode()
            self.input.listener.append(self.olgaMode)

        #self.SimonMode = myglobals.SimonMode
        #self.SimonMode.song.fromXml2file("Output.xml")




        #code.interact(local=locals())


        if self.song is None:
            self.song=MySong()
            #self.song.fromXml2file("Output.xml")

            self.song.fromXml2file(options.thescorefile)

            self.song.mystream.song = self.song


            self.song.mystream=self.song.mystream.decorate()
            #self.song.toXml2file(options.thescorefile +"_song.xml")


        if myglobals.SimonMode.song is None:
            myglobals.SimonMode.song = self.song


        if myglobals.OlgaMode.challenge is None:
            myglobals.OlgaMode.setknownNotesstream(self.song.mystream,None, 0.25)


        if myglobals.FeedBack is None:
            self.dontannoymefeedback = DontAnnoyMeFeedback(self.myMidiController)

        self.initdone = True


                

        # gui
        #app = MyApp()

    #while True:
    def updateGame(self,dt=0):
        #global self.analyseplay, ScreenState["Song"].challenge, self.allmymaps, self.bestmap, self.bestactive, self.perfect, self.newchallenge,\
        #self.output, self.output2, self.first, self.initdone, self.input, self.thescorefile, self.textGui, self.badmelodie, self.goodmelodie, self.playerror

        if not self.initdone:
            self.initGame()

        #self.input.pool()
        # pool in myMidiController
        self.myMidiController.update()
        #print "main " + str(self.input.inwort)


        # keyboard commands

        #chordreport = ChordReport(None)

        #self.allmymaps.findlastInputMap().rateNewTone()

         # ear training

        soundfeedback = True
        if soundfeedback:
            #pass
            self.dontannoymefeedback.update(None)

        if self.console:
              code.interact(local=locals())
              self.console=False

        infoLog.update()


    def edit(self):
        myglobals.ScreenState['ConfigObjectScreen'].object = myglobals.gameState
        #myglobals.ScreenState['ConfigObjectScreen'].object = myglobals.OlgaMode
        #myglobals.ScreenState['ConfigObjectScreen'].object = self.song
        myglobals.ScreenState.change_state('ConfigObjectScreen')


    def test(self, case = 17):

        if case == 17:
            a = MyStream()
            a.fromXml2file("./History/2014-08-18_21-37-16.071385.xml")
            self.myMidiController.defaultMidiin.replay(a)

        if case == 16:
            #myglobals.ScreenState['ConfigObjectScreen'].object = myglobals.SimonMode
            #myglobals.ScreenState['ConfigObjectScreen'].object = myglobals
            myglobals.ScreenState['ConfigObjectScreen'].object = myglobals.gameState
            #myglobals.ScreenState['ConfigObjectScreen'].object = myglobals.OlgaMode
            #myglobals.ScreenState['ConfigObjectScreen'].object = self.song
            myglobals.ScreenState.change_state('ConfigObjectScreen')


        if case == 15:
            asong=MySong()
            asong.fromXml2file("tests/284end.xml")
            si = MyStream()

            for x in asong.mystream:
                si.append(x)

            si.shift(0 - si[0].myoffset+1000)
            self.input.replay(si)


        if case == 14:

            #myglobals.ScreenState.change_state("Simon")
            myglobals.ScreenState.change_state("SimonViewBestActiveScreen")
            #anote = self.song.mystream[1196]
            myglobals.SimonMode.initSimonChallenges()
            #myglobals.SimonMode.initSimonChallenges(anote)
            #myglobals.SimonMode.update(None,None)

            asong=MySong()
            asong.fromXml2file("tests/284end.xml")
            si = MyStream()

            for x in asong.mystream:
                si.append(x)

            si.shift(0 - si[0].myoffset+1000)
            self.input.replay(si)


        if case == 13:
            #myglobals.ScreenState.change_state("Simon")
            myglobals.ScreenState.change_state("SimonViewBestActiveScreen")
            anote = self.song.mystream[1196]
            #myglobals.SimonMode.initSimonChallenges()
            myglobals.SimonMode.initSimonChallenges(anote)
            #myglobals.SimonMode.update(None,None)

            ti = MyStream()
            n = len(self.song.mystream)
            n = 1196
            count = 50

            #start = n-count
            start = n-count
            #print "test playing"
            for x in xrange(start ,n+count):
                anote  = MyNote()
                anote.midi = self.song.mystream[x].midi
                anote._myduration = self.song.mystream[x]._myduration
                #anote._myoffset = self.song.mystream[x]._myoffset * 0.25
                anote._myoffset = (self.song.mystream[x]._myoffset - self.song.mystream[start]._myoffset) * 1 + 1000
                anote._volume = self.song.mystream[x]._volume
                ti.append(anote)
                #print anote

            # ti.shift((0 - ti[0].myoffset) + 1000)

            print "playing "

            print ti.prettyprint()
            self.input.replay(ti)




        if case == 12:
            myglobals.ScreenState.change_state("SimonViewBestActiveScreen")
            myglobals.SimonMode.initSimonChallenges()

            ti = MyStream()
            n = len(self.song.mystream)
            count = n
            for x in xrange(n-count,n):
                anote  = MyNote()
                anote.midi = self.song.mystream[x].midi
                anote._myduration = self.song.mystream[x]._myduration
                anote._myoffset = self.song.mystream[x]._myoffset * 0.5
                #anote._myoffset = self.song.mystream[x]._myoffset * 1
                anote._volume = self.song.mystream[x]._volume
                ti.append(anote)

            ti.shift(0 - ti[0].myoffset)
            si = MyStream()

            count = len(self.song.startparts)+3
            for x in xrange(count):
                si = si.appendStream(ti, pause=2000)

            #myglobalutils.simpleconsole()
            #code.interact(local=locals())

            # silence
            self.myMidiController.output.midioutput= None

            self.input.replay(si)


        if case == 11:
            si = MyStream()
            for x in self.song.mystream:
                si.append(x)
            si.shift(0 - si[0].myoffset)
            self.input.replay(si)

        if case == 10:
            self.song=MySong()
            self.song.fromXml2file("Output.xml")

            s = MyStream()
            s.fromXml2file("olga_no_edges_kn.xml")

            s.song = self.song
            self.song.mystream=s

            myglobals.OlgaMode.setknownNotesstream(s)
            myglobals.OlgaMode.challenge.speedtol=0.0


            si = MyStream()


            si.fromXml2file("olga_no_edges_in.xml")
            si.shift(0 - si[0].myoffset)
            self.input.replay(si)


        if case == 1:
            self.song=MySong()
            self.song.fromXml2file("Output.xml")
            myglobals.OlgaMode.setknownNotesstream(self.song.mystream)
            #myglobals.OlgaMode.challenge.speedtol=0.0

            s = MyStream()
            s.fromXml2file("i.xml")
            self.input.replay(s)

        if case == 4:
            #self.song=MySong()
            #self.song.fromXml2file("Output.xml")
            #myglobals.OlgaMode.setknownNotesstream(self.song.mystream)

            s = MyStream()
            s.fromXml2file("i.xml")

            """
            # trimm
            s.shift(0 - s[0].myoffset)
            s.toXml2file("i.xml")
            """

            self.input.replay(s,shift=True)

        if case == 3:
            self.song=MySong()
            self.song.fromXml2file("Output.xml")

            s = MyStream()

            end = len(self.song.mystream)
            start = 0

            start = 3
            end = 20

            for x in range(start,end):
                n = self.song.mystream[x]
                s.append(n)

            s.song = self.song
            self.song.mystream=s
            myglobals.OlgaMode.setknownNotesstream(s)
            myglobals.OlgaMode.challenge.speedtol=0.0


            s = MyStream()


            s.fromXml2file("i2s.xml")
            s.shift(0 - s[0].myoffset)
            self.input.replay(s)


        # worst case
        if case == 2:
            self.song=MySong()

            #self.song.fromXml2file("Output.xml")

            so = MyStream()
            so.fromXml2file("midi40.xml")

            self.song.mystream=so
            so.song= self.song

            myglobals.OlgaMode.setknownNotesstream(so)
            #myglobals.OlgaMode.challenge.speedtol = 0.0


            s = MyStream()
            s.fromXml2file("midi60.xml")
            self.input.replay(s)

        if case == 5:
            self.song=MySong()

            #self.song.fromXml2file("Output.xml")

            so = MyStream()
            so.fromXml2file("jump_error_known60.xml")

            self.song.mystream=so
            so.song= self.song


            myglobals.OlgaMode.setknownNotesstream(so)

            myglobals.OlgaMode.challenge.speedtol=0.0


            s = MyStream()
            s.fromXml2file("jump_error_played60.xml")
            self.input.replay(s)


        if case == 6:
            self.song=MySong()

            #self.song.fromXml2file("Output.xml")

            so = MyStream()
            so.fromXml2file("test_kn_miss.xml")

            self.song.mystream=so
            so.song= self.song


            myglobals.OlgaMode.setknownNotesstream(so)

            #myglobals.OlgaMode.challenge.speedtol=0.0


            s = MyStream()
            s.fromXml2file("test_in_miss.xml")
            self.input.replay(s)




    def testdraw(self):
        ScreenState["SimonViewGraphScreen"].challenge = self.olgaMode.challenge
        ScreenState.change_state("SimonViewGraphScreen")

# The Game State "Manager"
myglobals.gameState=GameEngineRoot()