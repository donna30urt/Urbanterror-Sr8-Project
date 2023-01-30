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

__version__ = '1.0'
__author__ = 'donna30'

import b3
import b3.events
import b3.plugin

import requests
import json

class VpnblockerPlugin(b3.plugin.Plugin):
    requiresConfigFile = False

    # www.iphub.info
    apiKey2 = 'get ur own key'

    def onStartup(self):

        # Get admin plugin so we can register commands
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            # Can't start without admin plugin
            self.error('Could not find admin plugin')
            return

        self.registerEvent(self.console.getEventID('EVT_CLIENT_AUTH'), self.onAuth)
        self.registerEvent(self.console.getEventID('EVT_CLIENT_JOIN'), self.onChange)

    ####################################################################################################################
    #                                                                                                                  #
    #    Events                                                                                                        #
    #                                                                                                                  #
    ####################################################################################################################

    def onAuth(self, event):
        client = event.client

        if client.maxLevel >= 2:
            return

        client.setvar(self, 'lastannounce', 0)

        if self.testIphub(client.ip):
            self.vpnAction(client, True)

    def onChange(self, event):
        client = event.client

        if client.var(self, 'speclock').value:
            self.vpnAction(client)

    ####################################################################################################################
    #                                                                                                                  #
    #    Functions                                                                                                     #
    #                                                                                                                  #
    ####################################################################################################################

    def vpnAction(self, client, speclock=None):
        if speclock:
            client.setvar(self, 'speclock', True)

        self.console.write("forceteam %s spec" % client.cid)
        self.vpnAnnounce(client)

    def vpnAnnounce(self, client):
        res = self.console.time() - client.var(self, 'lastannounce').value
        if (res > 3):
            self.console.write("scc %s cp \"^3A ^1VPN^3/^1Proxy ^3has been detected for your connection\"" % client.cid)
            self.console.write("tell %s \"^3Please reconnect with your ^2real connection ^3in order to ^4play here.\"" % client.cid)
            self.console.write("tell %s \"^3If you are encountering any issues, contact ^6donna30#2710 ^3via ^5Discord.\"" % client.cid)
            client.setvar(self, 'lastannounce', self.console.time())

    def testIphub(self, ip):
        try:
            iphubrequest = 'http://v2.api.iphub.info/ip/%s' % ip
            req = requests.get(iphubrequest, headers={'X-Key':'get ur own key'}, timeout=3)
            if req.status_code == 200:
                result = req.json()
                if result["block"] == 1:
                    return(True)
                else:
                    return(False)
        except:
            return(False)
