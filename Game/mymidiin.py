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

#from music21 import *

#from myMapAlg import *
#from myLevenshtein import MyLevenshtein, MyLevenshteinChallenge
import heapq
from Game import myNote
from Game.myStream import ischordms, MyStream
#import options


import pygame
import pygame.midi

import logging

logger = logging.getLogger('mymidin')
hdlr = logging.FileHandler('./mymidin.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)



class MyMidiIn(object):
    mychord = None
    #inwort =  None
    def __init__(self):

        self.innotes=MyStream()
        self.mychord = []
        self.upwort=[]
        self.allupwort=[]



        self.pressedkeys={}
        self.releasewait=[]

        self.lastAppendtick=0

        self.input = None


        # clear old file
        #file = open("../midicaptur.txt","w+")
        #file.close()

        #file = open("../midicapturn.txt","w+")
        #file.close()


        self.midistreamheapreplay=[]

        self.listener=[]



    def getMeassuredVolume(self):

        n = min(len(self.innotes),5)

        sum = 0
        for x in range(n):
            sum = sum +self.innotes[x].volume

        return sum /  max(n,1)


    def replay(self, s, shift=True):
        for n1 in s:
            ntime = n1.myoffset
            if shift:
                ntime=ntime + pygame.midi.time()
                nnew = myNote.MyPlayedNote()
                nnew._midi=n1.midi
                nnew._myoffset=ntime
                nnew._myduration=n1.myduration
                nnew._volume=n1.volume
            else:
                nnew=n1
            #x.update(nnew,nnew.myoffset)
            heapq.heappush(self.midistreamheapreplay,(nnew.myoffset,nnew))



    def pool(self):
        if self.input:
            n1 = None

            #self.mychord =[]
            # time to seconds
            #tts = ((60.0*1000000.0/self.bpm)/self.resolution)/1000.0

            if self.input.poll():
                events =  self.input.read(10)
            else:
                events=[]

            #[[[128, 59, 64, 0], 2626965]] release
            #[[[144, 53, 64, 0], 2641038]] press

            for event in events:
                logger.info("event " + str(event))
                # velocity 0 release key on kawai mp10
                # event Noteoff
                #if (event.name == "Note On" and event.data[1] == 0) or event.name == "Note Off":
                # 16 channels
                if (event[0][0] >= 128  and event[0][0] < 128 +16) or ((event[0][0] >= 144 and event[0][0] < 144+16) and event[0][2]==0):
                    #(n1,self.pressedevent) = self.pressedkeys[event.data[0]]
                    try:
                        #n1,oldevent  = self.pressedkeys[(event[0][0],event[0][1])]

                        #del self.pressedkeys[(event[0][0],event[0][1])]
                        n1,oldevent  = self.pressedkeys[event[0][1]]
                        del self.pressedkeys[event[0][1]]
                        logger.debug("Note released " + str(n1.midi))
                    except:
                        logger.debug("Note released, but not pressed?? " + str(event))
                        # ignoring
                        continue
                        # wrong
                        #break
                    duration = event[1] - oldevent[1]
                    #file = open("midicapturn.txt","a+")
                    #file.write(str(self.pressedevent.tick) +" " +str(self.pressedevent.data) +"\n")
                    #file.close()

                    #n1.myduration=duration*tts
                    n1.myduration=duration

                    logger.debug("Note finished " + str(n1.__dict__))

                    #logger.info(str(n1.midi) +" myoffset:" +str(n1.myoffset)+"("+str(oldevent[1]) +") "+ str(n1.myduration)+" "+ str(n1.volume) +"\n")
                    #logger.info("lastappendtick "+ str(self.lastAppendtick))
                    #self.upwort.append([n1])

                #else:
                #if event.name == "Note On" and event.data[1] <> 0:
                if (event[0][0] >= 144 and event[0][0] < 144 +16) and event[0][2]!=0:
                    # event NoteOn

                    n1 = myNote.MyPlayedNote()
                    n1.midi=event[0][1]
                    n1.volume=event[0][2]
                    #n1.myoffset=event.tick*tts
                    n1.myoffset=event[1]

                    logger.debug("Note Played " + str(event) +" " + str(n1.__dict__))


                    n1.myduration = -1

                    # None doest work because None refetches from db
                    #n1.myduration = None

                    #self.pressedkeys[(event[0][0],n1.midi)]=(n1,event)

                    # ugly midi stream?
                    if not (n1.midi in self.pressedkeys):
                        self.pressedkeys[n1.midi]=(n1,event)
                        # chord detection, bad for myduration
                        #self.appendNote(n1)
                        self.lastAppendtick=event[1]

                        #logger.info("appending "+ str(n1))


                        for x in self.listener:
                            x.update(n1,n1.myoffset)
                        logger.debug("Note send to all listeners " + " " + str(n1.__dict__))

                        self.innotes.append(n1)
                    else:
                        logger.debug("Note pressed twice.. " + str(event) + " and " + str(self.pressedkeys[n1.midi][1]))


            if len(events) > 0:
                logger.debug("len(events) done" + " " + str(len(events)))



            # chord detection
            #tts = ((60.0*1000000.0/self.bpm)/self.resolution)/1000.0
            #dtick = (self.seq.queue_get_tick_time()-self.lastAppendtick)*tts
            dtick = pygame.midi.time()-self.lastAppendtick

            allready= True
            # no time ticks if notes are waiting
            allready= len(events) == 0
            #for x  in self.mychord:
            #    allready = allready and not x.myduration == -1


            if dtick > ischordms and allready:
                #self.lastAppendtick=self.seq.queue_get_tick_time()
                self.lastAppendtick=pygame.midi.time()
                #self.appendNote(None)


                ## a fake note
                #n1f = myNote.MyPlayedNote()

                ##n1.myoffset=event.tick*tts
                #n1f.myoffset=self.lastAppendtick

                #logger.info("lastappendtick no note "+ str(self.lastAppendtick))

                for x in self.listener:
                    x.update(None,self.lastAppendtick)


            # replay
            if len(self.midistreamheapreplay)>0:
                # take a peek
                n1 = heapq.heappop(self.midistreamheapreplay)[1]
                #heapq.heappush(self.midistreamheap, x)

                while True:
                    if n1.myoffset < pygame.midi.time():
                        #self.chunk.append(x[1])
                        #print "replaying " + n1.prettyprint(),
                        for x in self.listener:
                            #print "to  " + str(x)
                            x.update(n1,n1.myoffset)

                        if len(self.midistreamheapreplay)>0:
                            n1 = heapq.heappop(self.midistreamheapreplay)[1]
                        else:
                            break
                    else:
                        # repush
                        heapq.heappush(self.midistreamheapreplay, (n1.myoffset, n1))
                        break




