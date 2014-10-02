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



import hotshot
import signal
import code
import traceback


from kivy.clock import Clock
from Game import options

from Gui.visitingOlga import VisitingOlga

import myglobals



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


# more the gameloop and cause kivy wants to be the main loop updateGui:(
def updateGui(dt):
    #()
    myglobals.ScreenState.update()

def updateGame(dt):
    #prof.runcall(myglobals.gameState.updateGame)
    myglobals.gameState.updateGame()



if __name__ == '__main__':
    try:
        # TODO memory management
        #gc.disable()

        listen()
        """
        from guppy import hpy
        myglobals.hp = hpy()
        myglobals.hp.setrelheap()
        """


        myargs= (sys.argv[1:])
        if len(myargs) != 1:
            print "\nusage:"
            print "python main.py file"
            #print "file a music21 supported file (midi, musicxml ..)"
            print "file a Olga song file "
        else:

            options.optionsNeeded(myargs)
            #code.interact(local=locals())
            myglobals.gameState.updateGame()
            pianosimon = VisitingOlga()


            Clock.schedule_interval(updateGui, 1 / 10.)
            Clock.schedule_interval(updateGame, 1 / 25.)
            pianosimon.run()
            print "RUN FINISHED"
    except:
        console()

    prof.close()

    #stats = hotshot.stats.load("logicupdate.prof")
    #stats.sort_stats('cumulative', 'time', 'calls')
    #stats.print_stats(50)


