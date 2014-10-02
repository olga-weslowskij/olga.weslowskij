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
import sys

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)

import hotshot
import hotshot.stats

#prof = hotshot.Profile("logicupdate.prof")


if __name__ == '__main__':

    #prof.close()
    myargs= (sys.argv[1:])
    if len(myargs) != 1:
        stats = hotshot.stats.load("main.prof")
    else:
        stats = hotshot.stats.load(myargs[0])

    stats.sort_stats('cumulative', 'time', 'calls')
    #stats.sort_stats('time', 'calls')
    stats.print_stats(50)
