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
import code
import hotshot

import logging
from Game.myRunStateChallengeOlga import MyRunStateChallengeOlga
from Game.mySong import MySong
from Game.myStream import MyStream

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

import unittest

class TestRunstateChallenge(unittest.TestCase):

    def setUp(self):
        pass


    def test_KnChordLastNotMissing(self):
        prof = hotshot.Profile("test_2parts.prof")
        c = MyRunStateChallengeOlga()

        song=MySong()
        #self.song.fromXml2file("Output.xml")

        song.fromXml2file("/home/test/PycharmProjects/olga/Songs/OlgaXml/Juravlev.xml")

       # song.mystream.song = song
        #song.mystream=song.mystream.decorate()

        #c.jumpToStates.registerStream(song.mystream)

        c.update()
        oa=None

        invspeed = 1
        start = len(song.mystream)-20
        #start = 0
        end = len(song.mystream)


        #c.jumpToStates.registerStream([song.mystream[start]])
        c.jumpToStates.registerStream(song.mystream)


        #create inputstream
        sin=MyStream()
        # missing last chord
        for i in xrange(start,end-1):
            x = song.mystream[i]
            nn = x.note.clone()
            nn.myoffset = (- song.mystream[start].myoffset + nn.myoffset) * invspeed
            sin.append(nn)


        prof.start()
        for j in sin:
            c.add_note(j)
            c.update()
            print str(j) + " done"
            try:
                print "bestRunOnIn " + c.bestRunOnIn[c.innotes[-1]].peek().prettyprint()
            except Exception as e:
                print(e)
                code.interact(local=locals())
            oa = c.bestActive()


            #print c.bestActive().prettyprint(history=False),


        #or in xrange(100):
        i = 5
        c.updatePause(sin[-1].myoffset + i * 50)



        prof.stop()
            #print oa.prettyprint(history=True)
        #print oa.prettyprint(history=True)


        #print c.bestActive().prettyprint(history=True)
        print "All Done"
        print c.bestActive().prettyprint(history=True)

        print (oa.errors[0])

        self.assertEqual(len(oa.errors) > 0 , True)

        self.assertEqual(oa.errors[0].__class__.__name__,"KnChordInTimeTooLate")

        # should raise an exception for an immutable sequence
        #self.assertRaises(TypeError, random.shuffle, (1,2,3))


"""
    def test_2parts(self):

        prof = hotshot.Profile("test_2parts.prof")
        c = MyRunStateChallengeOlga()


        song=MySong()
        #self.song.fromXml2file("Output.xml")

        song.fromXml2file("/home/test/PycharmProjects/olga/Songs/OlgaXml/Juravlev.xml")

       # song.mystream.song = song
        #song.mystream=song.mystream.decorate()

        #c.jumpToStates.registerStream(song.mystream)

        c.update()
        oa=None

        invspeed = 1
        start = len(song.mystream)-20
        start = 0
        end = len(song.mystream)




        #c.jumpToStates.registerStream([song.mystream[start]])
        c.jumpToStates.registerStream(song.mystream)



        #create inputstream
        sin=MyStream()
        for i in xrange(start,end):
            x = song.mystream[i]

            nn = x.note.clone()

            nn.myoffset = (- song.mystream[start].myoffset + nn.myoffset) * invspeed

            sin.append(nn)
        print "sin.prettyprint()"
        #print sin.prettyprint()
        print "sin.prettyprint() done"



        sc= MyStream()

        for j in xrange(1):
            sc = sc.appendStream(sin,pause = 500 ,speed=invspeed)

        #print sc.prettyprint()

        prof.start()
        for j in sc:
            c.add_note(j)
            c.update()
            print str(j) + " done"
            try:
                print "bestRunOnIn " + c.bestRunOnIn[repr(c.innotes[-1])].peek().prettyprint()
            except:
                pass
                #code.interact(local=locals())
            oa = c.bestActive()
            #print c.bestActive().prettyprint(history=False),


        prof.stop()
            #print oa.prettyprint(history=True)
        #print oa.prettyprint(history=True)


        #print c.bestActive().prettyprint(history=True)
        print "All Done"
        print c.bestActive().prettyprint(history=True)


        self.assertEqual(oa.rspeed(), 1/invspeed)

        # should raise an exception for an immutable sequence
        #self.assertRaises(TypeError, random.shuffle, (1,2,3))



    def test_apart(self):
        c = MyRunStateChallenge()
        song=MySong()
        #self.song.fromXml2file("Output.xml")

        song.fromXml2file("../Songs/OlgaXml/Juravlev.xml")

       # song.mystream.song = song
        #song.mystream=song.mystream.decorate()

        c.jumpToStates.registerStream(song.mystream)

        print "go"
        c.update()
        oa=None

        invspeed =.75
        start = len(song.mystream) -20
        #start = 0
        end = len(song.mystream)
        for i in xrange(start,end):
            x = song.mystream[i]


        #for x in song.mystream:
            nn = x.note.clone()
            nn.myoffset = nn.myoffset * invspeed
            c.add_note(nn)
            c.update()

            if c.bestActive() is None:
                #print str(x)
                break
            else:
                #print str(x)
                oa = c.bestActive()

        print "Done"
        #print oa.prettyprint(history=True)
        #print c.bestActive().prettyprint(history=True)


        self.assertEqual(oa.rspeed(), 1/invspeed)

        # should raise an exception for an immutable sequence
        #self.assertRaises(TypeError, random.shuffle, (1,2,3))

"""

if __name__ == '__main__':
    unittest.main()

    #c = TestRunstateChallenge()

    #c.test_2parts()