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
import heapq
from myglobals import ScreenState
from Game.myStream import MyStream
import myglobals
#import gameEngineRoot
import logging


logger = logging.getLogger('SimonRequests')
hdlr = logging.FileHandler('./simonRequests.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)





def ShowChallenge(achallenge=None, newpart=False, part = None):
    #levcha = MyLevenshteinChallenge()
    #levcha = ScreenState["Song"].levcha2
    if myglobals.SimonMode.activeChallenge() is None:
        ret = MyStream()
        return ret

    #end = myglobals.SimonMode.activeChallenge().challenge.challengeendnote
    end = myglobals.SimonMode.activeChallenge().challenge.challengeendnote
    start = myglobals.SimonMode.activeChallenge().challenge.challengestartnote

    #ret = MyStream()
    #ret = myglobals.SimonMode.activeChallenge().challenge.knownStream()
    #ret = myglobals.SimonMode.activeChallenge().challenge.knownStream()
    if newpart:
        ret = myglobals.SimonMode.activeChallenge().newpart
        #print "SimonRequest len(ret) " , len(ret)
    else:
        ret = myglobals.SimonMode.activeChallenge().allpart

    if not (part is None):
        try :
            ret = myglobals.SimonMode.activeChallenge().__getattribute__(part)
        except:
            pass

    ScreenState["SimonViewChallengeScreen"].notesscroller.run = ret
    ScreenState["SimonViewChallengeScreen"].dirty = True
    ScreenState.change_state("SimonViewChallengeScreen")

    return ret

def playChallenge(part = None):
    #end = myglobals.SimonMode.activeChallenge().challenge.challengeendnote
    end = myglobals.SimonMode.activeChallenge().challenge.challengeendnote
    start = myglobals.SimonMode.activeChallenge().challenge.challengestartnote

    #ret = MyStream()
    #ret.build(start, end)

    ret = myglobals.SimonMode.activeChallenge().allpart

    if not (part is None):
        try :
            ret = myglobals.SimonMode.activeChallenge().__getattribute__(part)
        except:
            pass

    speed=myglobals.SimonMode.activeChallenge().speed

    if speed is None:
        speed =1.0

    stream=ret


    output = myglobals.gameState.myMidiController.getMidiOut()
    if len(stream)>0:
        output.playpartMyStream(stream , 0 , len(stream), startnote=stream.notes[0],speed=speed)

def playNewPart():
    #end = myglobals.SimonMode.activeChallenge().challenge.challengeendnote
    #end = myglobals.SimonMode.activeChallenge().
    #if end is None:
    #    end = myglobals.SimonMode.activeChallenge().challenge.challengeendchord.notes[-1]
    #start = myglobals.SimonMode.activeChallenge().challenge.challengestartnote

    #logger.info("playNewPart " +str(start)+ " to " + str(end))

    #ret = MyStream()
    #ret.build(start, end)

    stream=myglobals.SimonMode.activeChallenge().newpart


    speed=1.0
    output = myglobals.gameState.myMidiController.getMidiOut()
    if len(stream) >0:
        output.playpartMyStream(stream , 0 , len(stream), startnote=stream.notes[0],speed=speed)



def playNewPartArp():
    end = myglobals.SimonMode.activeChallenge().challenge.challengeendnote
    if end is None:
        end = myglobals.SimonMode.activeChallenge().challenge.challengeendchord.notes[-1]
    start = myglobals.SimonMode.activeChallenge().challenge.challengestartnote


    #ret = MyStream()

    #ret.build(start, end)

    ret=myglobals.SimonMode.activeChallenge().newpart

    stream=ret.splitChords()
    if len(stream)>0:
        speed=1.0
        output = myglobals.gameState.myMidiController.getMidiOut()
        output.playpartMyStream(stream , 0 , len(stream), startnote=stream.notes[0],speed=speed)


def setSong(aSong):
    myglobals.SimonMode.activeChallenge().challenge = None
    myglobals.SimonMode.activeChallenge().challenge = None
    myglobals.SimonMode.song=aSong




def createShowErrorStream():

    #print "createShowErrorStream"
    #achallenge = ScreenState["Song"].levcha

    """

    l=myglobals.OlgaMode.challenge.lasterrors

    #vb = myglobals.SimonMode.activeChallenge().challenge.bestActive()



    va = None
    if len(l)>0:
        va = l[-1]
    else:
        ScreenState["SimonViewErrorScreen"].notesscroller.run = None
    """
    va = myglobals.OlgaMode.challenge.bestabsrun

    if va:

        ScreenState["SimonViewErrorScreen"].notesscroller.run = va
        #ScreenState["SimonViewErrorScreen"].dirty = True
        #ScreenState.change_state("SimonViewErrorScreen")
        return
    else:
        return


    bchallenge = myglobals.SimonMode.activeChallenge().challenge


    if len(bchallenge.lasterrors) >0:
        toexpand = bchallenge.lasterrors[-1]
    else:
        print "no Error"
        return

    #code.interact(local=locals())

    #pdb.set_trace()

    tmpchall = MyLevenshteinChallengeAbsError()

    tmpchall.name= "ShowError"

    tmpchall.myadd_node(toexpand)


    heapq.heappush(tmpchall.fringe, (bchallenge.seen[toexpand], toexpand))
    tmpchall.seen[toexpand] = bchallenge.seen[toexpand]
    tmpchall.seen[toexpand.startRun] = bchallenge.seen[toexpand.startRun]



    #tmpchall.paths[toexpand] = [toexpand]
    tmpchall.starterrors[toexpand.startRun] = bchallenge.starterrors[toexpand.startRun]
    # expand till end of input?
    #tmpchall.maxerror = bchallenge.seen[toexpand]+1

    tmpchall.bestabsrun = toexpand
    #tmpchall.bestError = bchallenge.starterrors[toexpand.startRun] + bchallenge.seen[toexpand]
    tmpchall.speedtol = bchallenge.speedtol


    tmp = toexpand.currentMelodyRating.notenextMapping.knownChord

    if toexpand.currentMelodyRating.notenextMapping.chordfull():
        if  toexpand.nextKnownChordFirstNote():
            tmp = toexpand.nextKnownChordFirstNote().chord




    logger.info("expanding till" + str(tmp.prettyprint()) )


    tmpchall.retondone = (None, tmp)

    tmpchall.targets=[tmpchall.retondone]
    tmpchall.maxerror = None


    v = None

    logger.info("expanding error " + str(toexpand) )
    v = tmpchall.update()
    logger.info("expanding error  done " )

    """
    tmpchall.maxerror=tmpchall.seen[v]
    heapq.heappush(tmpchall.fringe, (bchallenge.seen[toexpand], toexpand))

    v = tmpchall.update()
    """



    code.interact(local=locals())


    #tmpchall.chain(toexpand)

    # not needed anymore? TODO bestabsrun should be really the best not only if not active
    if v is None:
        print "v = tmpchall.bestabsrun"
        v = tmpchall.bestabsrun

    ScreenState["SimonViewErrorScreen"].notesscroller.run = v
    ScreenState["SimonViewErrorScreen"].dirty = True

    """
    if v:

        ret = v.list

        #for x in ret
        #    x.errostr= v.errorstrs[x]

        logger.info("error stream: " + str(ret))

        ret2 = myRatingSingleNote()
        ret2.map = False
        ret2.noteratings = ret

        ScreenState["SimonViewErrorScreen"].notesscroller.rating = ret2
        ScreenState["SimonViewErrorScreen"].dirty = True


    """
    pass




def createShowMissingStream(bchallenge):
    #print "createShowErrorStream"
    #achallenge = ScreenState["Song"].levcha

    bchallenge = myglobals.SimonMode.activeChallenge().challenge
    #print (len(achallenge.G.node))
    logger.info("creating Missing Stream" )

    achallenge, dones = bchallenge.findsolution()

    #code.interact(local=locals())

    ScreenState["SimonViewGraphScreen"].challenge=achallenge
    ScreenState["SimonViewGraphScreen"].dirty = True
    #TODO why split screen??
    #ScreenState.change_state("SimonViewGraphScreen")


    if len(dones) == 0:
        logger.info("No solution found")
        ScreenState["SimonViewMissingScreen"].notesscroller.rating = None
        ScreenState["SimonViewMissingScreen"].dirty = True
        return


    #print (len(achallenge.G.node))
    v = min(dones, key= lambda a: (achallenge.seen[a], len(a.list)))
    #v = achallenge.donelist[0]

    donesseen=[]
    for x in dones:
        donesseen.append([x,achallenge.seen[x]])

    logger.info("achallenge.dones " + str(donesseen) )



    logger.info("v (Best Challenge)"  + str(v) )

    ret = v.list

    #for x in ret:
    #    x.errostr= v.errorstrs[x]

    logger.info("error stream: " + str(ret))

    """
    ScreenState["SimonViewMissingScreen"].notesscroller.rating = ret2
    ScreenState["SimonViewMissingScreen"].dirty = True
    """

    return ret

def createShowDoneStream(bchallenge):
    #print "createShowErrorStream"
    #achallenge = ScreenState["Song"].levcha
    if myglobals.SimonMode.lastDoneChallenge() is None:
        return

    if myglobals.SimonMode.lastDoneChallenge().doneRun is None:
        return

    v =  myglobals.SimonMode.lastDoneChallenge().doneRun

    """
    achallenge = myglobals.SimonMode.lastDoneChallenge().challenge
    #print (len(achallenge.G.node))
    logger.info("creating done Stream" )

    dones = achallenge.donelist.get(achallenge.targets[-1],[])
    if len(dones) == 0:
        logger.info("No solution found")
        return

    #print (len(achallenge.G.node))
    v = min(dones, key= lambda a: (achallenge.seen[a], len(a.list)))
    #v = achallenge.donelist[0]
    """


    #for x in ret:
    #    x.errostr= v.errorstrs[x]

    logger.info("soltution stream: " + str(v))


    ScreenState["SimonViewDoneScreen"].notesscroller.run = v
    ScreenState["SimonViewDoneScreen"].dirty = True
    #ScreenState.change_state("SimonViewDoneScreen")
    return v



def ShowInStream(chall=None):
    v = myglobals.SimonMode.activeChallenge().challenge.innotes
    ScreenState["Simon"].notesscroller.stream = v
    ScreenState["Simon"].dirty = True
    #ScreenState["Simon"].update=ShowInStream
    ScreenState.change_state("Simon")
    return v





def createShowBestActiveStream(bchallenge=None):
    ScreenState.change_state("SimonViewBestActiveScreen")

    va = myglobals.SimonMode.activeChallenge().challenge.bestActive()
    #vb = myglobals.SimonMode.activeChallenge().challenge.bestActive()

    if va:
        logger.info("Best Acitve stream: " + str(va.prettyprint()))
        #l.append(va)
    else:
        logger.info("Best Acitve stream: " + str(None))

    return va



