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
import pygame
import pygame.midi

from mylibs import myList

"""
midiin_device = 4 ; midiout_device = 2;

pygame.init()

pygame.midi.init()
i = pygame.midi.Input(midiin_device)
o = pygame.midi.Output(midiout_device)



for x in range(pygame.midi.get_count()):
    print str(x)+ " " + str(pygame.midi.get_device_info(x))

mt = None
going = True
while going:
    if i.poll():
        midi_events = i.read(10)
        print midi_events
"""





class MyMidiOut:
    def __init__(self,aoutput=None):
        #self.output=pygame.midi.Output(midiout_device)
        self.output=aoutput

        self._streamendtick=None


    @property
    def streamendtick(self):
        if self._streamendtick > pygame.midi.time():
            return self._streamendtick
        else:
            return pygame.midi.time()

    def playpartMyStream(self, mychords,istart=0,iend=None, startnote=None, startchord=None ,speed = 1.0, starttick = None):

        # we first shift and then scale by speed

        if istart == iend:
            start = istart
            end = iend+1
        else:
            start = istart
            end = iend

        astarttick = 0

        if startnote:
            #astarttick = startchord.midiEvent(0, 1.0)[0][1]
            astarttick = startnote.midiEvent(0, speed)[0][1]


        if startchord:
            if type(startchord) is list or type(startchord) is myList:
                #print "startnode " + str(startchord)# + " " + str(startchord.myoffset)
                minshift = startchord[0].midiEvent(0, 1.0)[0][1]
                for tmp in startchord:
                    minshift = min(tmp.midiEvent(0, 1.0)[0][1], minshift)
                astarttick = minshift

        #print "astarttick " + str(astarttick)

        if not end:
            end = len(mychords)

        mystream=[]
        #mystream=pmidi.Track()
        #noteonoff={}

        if starttick:
            abstimetick = starttick
        else:
            abstimetick = pygame.midi.time()
        #abstimetick = 0


        #mychordspart=mychords[start:len(mychords)]
        mychordspart=mychords[start:end]

        # 1024 midi events fixed
        #if len(mychordspart) > 550:
        #print "cant handle streams > 550 at the current version"
        #print "playing " + str(len(mychordspart)) +" notes"

        #mychords.show('text')
        #mychordspart.show('text')

        #newbpm = self.bpm


        if self.streamendtick:
            endtime = max(abstimetick-astarttick, self.streamendtick)
        else:
            endtime = abstimetick-astarttick

        for tmp in mychordspart:
            # chodify
            if type(tmp) is list:
                for tmp2 in tmp:
                    ret = tmp2.midiEvent(abstimetick-astarttick, speed)
                    endtime = max(ret[1],endtime)
                    mystream.extend(ret)
            #print tmp.fullName
            #normal
            else:
                #ret = tmp.midiEvent(self.bpm, self.myresolution,abstimetick-astarttick, mystream)
                ret = tmp.midiEvent(abstimetick-astarttick,speed)
                endtime = max(ret[1][1],endtime)
                mystream.extend(ret)

        self._streamendtick = endtime

        #elf.seq.set_nonblock(nonblock=False)
        #for tmp2 in mystream:
        #        print tmp2
            #print "mymidiout " + str(tmp2)
            #pass

        if self.output:
            self.output.write(mystream)


            #self.seq.event_write(tmp2,tick=False)
            #play(mystream)

        #self.seq.start_sequencer()





