import code
import heapq
import pygame
from Game import options
from Game.mymidiin import MyMidiIn
from Game.mymidiout import MyMidiOut


class MyMidiController(object):

    def __init__(self):
        self.midiin_device = 3
        self.midiout_device = 2

        self.defaultMidiin = MyMidiIn()
        self.output=MaxMidiOut()

        pygame.init()
        pygame.midi.init()

        #self.defaultMidiin=None

        #options.RecommendOptionsValues["midi in"]={}
        #options.RecommendOptionsValues["midi out"]={}

        # build options

        for x in range(pygame.midi.get_count()):
            (interf, name, input, output, opened) = pygame.midi.get_device_info(x)
            #print "midi devices " + str((interf, name, input, output, opened))

            if input==1:
                options.RecommendOptionsValues["midi in"][name]=x

            if output==1:
                options.RecommendOptionsValues["midi out"][name]=x


        self.built = False

    def build(self):
        self.midiin_device= options.getOptionValue("midi in")
        self.midiout_device= options.getOptionValue("midi out")
        self.input = pygame.midi.Input(self.midiin_device)
        self.defaultMidiin.input= self.input
        # latency 1: to respect timestamp
        self.output.midioutput=pygame.midi.Output(self.midiout_device,1)

        #self.output.midioutput.

    def getMidiIn(self):
        return self.defaultMidiin

    def getMidiOut(self):
        ret = MyMidiOut(self.output)
        return ret


    def update(self):
        self.output.update()
        self.getMidiIn().pool()


    def getMidiTick(self):
        return pygame.midi.time()


# delay midi output, we can only send 1024 events to the queue
# we send 1 sec chunks
class MaxMidiOut(object):
    def __init__(self):
        self.midistreamheap=[]
        self.midioutput=None
        self.played=[]

    def write(self, alist):
        #print "MaxMidiOut write" + str(alist)
        for x in alist:
            #x[1] == tick
            heapq.heappush(self.midistreamheap,(x[1],x))

    def update(self):
        #print "MaxMidiOut update"
        if len(self.midistreamheap)>0:
            self.chunk=[]
            ticktime=pygame.midi.time()
            # take a peek
            x = heapq.heappop(self.midistreamheap)
            #heapq.heappush(self.midistreamheap, x)



            while True:
                if x[0]-ticktime < 1000:
                    #print "MaxMidiOut playing  " +str(x[1])
                    self.chunk.append(x[1])
                    # debug midiout overflow
                    self.played.append([x[1]])
                    if len(self.midistreamheap)>0:
                        x = heapq.heappop(self.midistreamheap)
                    else:
                        break
                else:
                    # repush
                    heapq.heappush(self.midistreamheap, x)
                    break


            if self.midioutput:
                try:
                    self.midioutput.write(self.chunk)
                except:
                    print "midioutput overflow"
                    code.interact(local=locals())
                    pass


if __name__ == "__main__":

    midiController = MyMidiController()
    input=midiController.getMidiIn()
    while (True):
        input.pool()