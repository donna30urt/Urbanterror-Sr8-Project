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
import re
import b3.events
import b3.plugin
import urllib
import ipinfo

class CoblockerPlugin(b3.plugin.Plugin):
    requiresConfigFile = False

    #Getting Plugin admin (cannot register commands without it)
    def onStartup(self):
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            self.error('Could not find admin plugin')
            return

        # Registering events
        self.registerEvent(self.console.getEventID('EVT_CLIENT_JOIN'), self.onJoin)
        
    ####################################################################################################################
    #                                                                                                                  #
    #    Events                                                                                                        #
    #                                                                                                                  #
    ####################################################################################################################

    def onJoin(self, event):
        client = event.client        
        
        if (client.connections <= 50 and client.maxLevel < 20 and not client.bot):
            ip = str(client.ip)
            access_token = 'get-ur-own-key'
            
            handler = ipinfo.getHandler(access_token)
            
            details = handler.getDetails(ip)
            
            # make a list of blocked cities and countries
            
            blockedCity = "Cartagena"
            blockedCountry = "Colombia"
            
            blockedCity2 = "Saint-.tienne"
            blockedCountry2 = "France"
            
            clCity = details.city
            clCountry = details.country_name
            
            if (clCity == blockedCity and clCountry == blockedCountry):
                self.console.write("forceteam %s spec" % client.cid)
                self.console.write("^6[^5d3frk City Blocker^6] ^1UNSAFE ^3connection from %s" % client.name)
                client.message("^6[^5d3frk City Blocker^6] ^1UNSAFE ^3connection detected")
                client.message("^3Join the discord and get^1Authorized ^3to play on this server")
                
            elif (clCity == blockedCity2 and clCountry == blockedCountry2):
                self.console.write("forceteam %s spec" % client.cid)
                self.console.write("^6[^5d3frk City Blocker^6] ^1UNSAFE ^3connection from %s" % client.name)
                client.message("^6[^5d3frk City Blocker^6] ^1UNSAFE ^3connection detected")
                client.message("^3Join the discord and get^1Authorized ^3to play on this server")