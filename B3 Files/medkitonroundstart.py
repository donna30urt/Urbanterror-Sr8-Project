# ################################################################### #
#                                                                     #
#  BigBrotherBot(B3) (www.bigbrotherbot.net)                          #
#  Copyright (C) 2005 Michael "ThorN" Thornton                        #
#                                                                     #
#  This program is free software; you can redistribute it and/or      #
#  modify it under the terms of the GNU General Public License        #
#  as published by the Free Software Foundation; either version 2     #
#  of the License, or (at your option) any later version.             #
#                                                                     #
#  This program is distributed in the hope that it will be useful,    #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of     #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the       #
#  GNU General Public License for more details.                       #
#                                                                     #
#  You should have received a copy of the GNU General Public License  #
#  along with this program; if not, write to the Free Software        #
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA      #
#  02110-1301, USA.                                                   #
#                                                                     #
# ################################################################### #
__author__ = 'donna30'
__version__ = '1.0'

import b3
import b3.events
import b3.plugin
import random, string
import random as rand


class MedkitonroundstartPlugin(b3.plugin.Plugin):
    requiresConfigFile = False

    #Getting Plugin admin (cannot register commands without it)
    def onStartup(self):
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            self.error('Could not find admin plugin')
            return

        # Registering events
        self.registerEvent(self.console.getEventID('EVT_GAME_ROUND_START'), self.onRoundstart)

    ####################################################################################################################
    #                                                                                                                  #
    #    Events                                                                                                        #
    #                                                                                                                  #
    ####################################################################################################################


    def onRoundstart(self, event):
        REDPLAYERS = {}
        BLUEPLAYERS = {}

        for client in self.console.clients.getList():
            team = self.console.write("getplayerteam %s" % client.cid)
            if "RED" in team:
                REDPLAYERS[client.name] = client.cid
            elif "BLUE" in team:
                BLUEPLAYERS[client.name] = client.cid
    
        if len(REDPLAYERS) + len(BLUEPLAYERS) >= 6:
            redplayer, redcid = random.choice(list(REDPLAYERS.items()))
            blueplayer, bluecid = random.choice(list(BLUEPLAYERS.items()))
            self.console.write("giveitem %s medkit" % redcid)
            self.console.write("giveitem %s medkit" % bluecid)
            self.console.write("bigtext \"^1%s ^3and ^4%s/n^6spawned ^3with a ^2Medkit ^3this round\"" % (redplayer, blueplayer))
