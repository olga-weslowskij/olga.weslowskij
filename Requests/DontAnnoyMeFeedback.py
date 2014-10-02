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
from Game import options
from Game.mySong import MySong
from Game.myStream import MyStream
import myglobals


logger = logging.getLogger('dontAnnoyMeFeedback')
hdlr = logging.FileHandler('./dontAnnoyMeFeedback.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)



class DontAnnoyMeFeedback(object):

    def __init__(self, myMidiController):
        self.goodmelodie = MySong()
        #self.goodmelodie.frommusic21('./Sounds/Good.xml')
        #self.goodmelodie.toXml2file('./Sounds/newGood.xml')

        self.goodmelodie.fromXml2file('./Sounds/newGood.xml')



        self.badmelodie = MySong()
        #self.badmelodie.frommusic21('./Sounds/Bad.xml')
        #self.badmelodie.toXml2file('./Sounds/newBad.xml')
        self.badmelodie.fromXml2file('./Sounds/newBad.xml')

        self.badtiming = MySong()
        #self.badtiming.frommusic21('./Sounds/BadTiming.xml')
        #self.badtiming.toXml2file('./Sounds/newBadTiming.xml')
        self.badtiming.fromXml2file('./Sounds/newBadTiming.xml')

        self.myMidiController = myMidiController

        self.chord=None

        self.outputstream=MyStream()

        self.FeedbackonPause = None

        #self.challenges=[]

        self.lastplayedError=None

        self.dones={}

        myglobals.FeedBack=self

        self.appendPause = 100
        self.ignoreFeedbackTimeAfterError = 500

        self.errorvolume=None

    def update(self, chordreport):
        if not self.FeedbackonPause:
                self.FeedbackonPause = self.myMidiController.getMidiOut()


        """
        # pause detection in olga??
        paused= True
        for x in self.challenges:
            paused = paused and x.paused

        ntmp = self.myMidiController.getMidiIn().innnotes
        if len(ntmp) > 0:
            if aTime -ntmp[-1] > appendPause:
                paused = True
                paused = paused and myglobals.SimonMode.activeChallenge().challenge.checkPause()
        """

        """ pause detection in MidiController
        too look for still pressed keys ??
        """

        paused = myglobals.OlgaMode.checkPause(self.myMidiController.getMidiTick())
        #logger.info("Olga paused? " + str(paused))

        if paused and len(self.outputstream) > 0:
            logger.info("Playing Feedback in the Pause now")
            playstream = self.outputstream
            self.FeedbackonPause.playpartMyStream(playstream, 0 , len(playstream), playstream[0], starttick = self.FeedbackonPause.streamendtick)
            self.outputstream = MyStream()


    def playError(self, stream, polite = False):
        #if not options.getOptionValue("mode") == "log":

        if polite and self.lastplayedError and self.lastplayedError + self.ignoreFeedbackTimeAfterError > self.myMidiController.getMidiTick():
            logger.info("playError  polilty not played")
            return

        logger.info("playError " +  str(polite)+   " politetime "  +  str(self.lastplayedError)  + " " +  str(
            self.ignoreFeedbackTimeAfterError) +" > "  + str(self.myMidiController.getMidiTick()))

        if True:
            self.feedbackoutput = self.myMidiController.getMidiOut()
            playstream = self.adjustVolume(stream)
            self.feedbackoutput.playpartMyStream(playstream, 0 , len(playstream), playstream[0])
            self.lastplayedError = self.myMidiController.getMidiTick()



    def playTimingError(self, polite = False):
        self.playError(self.badtiming.mystream, polite=polite)


    def playMelodieError(self, polite = False):
        self.playError(self.badmelodie.mystream, polite=polite)

    def playGoodMelodie(self):
        if True:
            if not self.FeedbackonPause:
                self.FeedbackonPause = self.myMidiController.getMidiOut()

            playstream = self.adjustVolume(self.goodmelodie.mystream)
            ret = MyStream()
            ret.appendStream(playstream, shift = - playstream[0].myoffset)

            self.outputstream.appendStream(ret, pause = self.appendPause)


    def playOnPause(self, stream, speed = 1.0):
        if not options.getOptionValue("mode") == "log":
            if not self.FeedbackonPause:
                self.FeedbackonPause = self.myMidiController.getMidiOut()

            playstream = stream
            ret = MyStream()
            ret.appendStream(playstream, shift = - playstream[0].myoffset , speed=1)

            ret2 = MyStream()
            ret2.appendStream(ret, shift = - ret[0].myoffset , speed=speed)

            self.outputstream.appendStream(ret2, pause = self.appendPause)



    def adjustVolume(self, stream):

        errorvolume = min(self.myMidiController.getMidiIn().getMeassuredVolume() +10,127)

        if self.errorvolume:
            errorvolume=self.errorvolume

        tmpstream= MyStream()
        for y in stream:
            x=y.clone()
            tmpstream.notes.append(x)
            x.volume = errorvolume

        return tmpstream


