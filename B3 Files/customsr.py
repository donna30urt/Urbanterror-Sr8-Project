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

from threading import Timer

class CustomsrPlugin(b3.plugin.Plugin):
    requiresConfigFile = False

    counter = 0

    def onStartup(self):
        # Get admin plugin so we can register commands
        self.query = self.console.storage.query
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            # Something is wrong, can't start without admin plugin
            self.error('Could not find admin plugin')
            return

        # Register events
        self.registerEvent(self.console.getEventID('EVT_CLIENT_JOIN'), self.onChange)
        # Register commands
        self._adminPlugin.registerCommand(self, 'funremove', 20, self.cmd_funremove, 'funfree')
        #self._adminPlugin.registerCommand(self, 'auth', 1, self.cmd_auth, 'auth')
        #self._adminPlugin.registerCommand(self, 'xlrtopstats', 1, self.cmd_xlrtopstats, 'xlrtop')
        self._adminPlugin.registerCommand(self, 'rank', 1, self.cmd_rank, 'rk')
        self._adminPlugin.registerCommand(self, 'rs', 1, self.cmd_resetscore, 'resetscore')
        self._adminPlugin.registerCommand(self, 'hi', 1, self.cmd_bhi, 'hello')
        self._adminPlugin.registerCommand(self, 'hiall', 1, self.cmd_bhiall, 'helloall')
        self._adminPlugin.registerCommand(self, 'help', 0, self.cmd_help, 'h')
        self._adminPlugin.registerCommand(self, 'discord', 0, self.cmd_discord, 'disc')
        #self._adminPlugin.registerCommand(self, 'nextmap', 1, self.cmd_mapinfo, 'mapinfo')

    def onChange(self, event):
        client = event.client
        self.console.write("forcecvar %s name %s" % (client.cid, client.name))

    def cmd_resetscore(self, data, client, cmd=None):
        self.console.write('setscore %s 0' % client.cid)
        self.console.write('setdeaths %s 0' % client.cid)

    def cmd_xlrtopstats(self, data, client, cmd=None):

        q = "SELECT * FROM `xlr_playerstats` ORDER BY `xlr_playerstats`.`skill` DESC limit 3"

        if data:
            if isinstance(data, int):
                if data	> 10:
                    client.message('^3!xlrtopstats ^110 ^3is the ^1Maximum.')
                    return
                else:
                    q = "SELECT * FROM `xlr_playerstats` ORDER BY `xlr_playerstats`.`skill` DESC limit %s" % data

        cursor = self.query(q)
        if cursor:
            while not cursor.EOF:
                self.counter += 1
                row = cursor.getRow()
                xclnt = self._adminPlugin.findClientPrompt(int(row['client_id']), client)
                message = "^3# %s: ^7%s : Skill ^3%s ^7Ratio ^5%s ^7Kills: ^2" % (self.counter, xclnt.name, int(row['skill']), int(row['ratio']), int(row['kills']))
                cmd.sayLoudOrPM(client, message)
                cursor.moveNext()
        cursor.close()
        self.counter = 0


    def cmd_rank(self, data, client, cmd=None):

        """\

        [<name>] - list a players Rank Position
        """
        if data:
            sclient = self._adminPlugin.findClientPrompt(data, client)
            if not sclient: return
        else:
            sclient = client
        id = sclient.id

        q = 'SELECT client_id, skill, FIND_IN_SET( skill, ( SELECT GROUP_CONCAT(DISTINCT skill ORDER BY skill DESC) FROM xlr_playerstats ) ) AS rank FROM xlr_playerstats WHERE client_id=%s' % (id)

        cursor = self.query(q)
        if not cursor.EOF:
            r = cursor.getRow()       
            message = '^7[^6XLR-^3Rank^7]: %s ^6-> Rank ^2%s' % (sclient.exactName, int(r['rank']))
            cmd.sayLoudOrPM(client, message)
            return
        else:
            message = '^7[^6XLR-^3Rank^7]:^7 %s ^6-> ^1NOT Ranked' % sclient.exactName
            cmd.sayLoudOrPM(client, message)
        return  


    def cmd_discord(self, data, client, cmd=None):
        self.console.say("^5Discord: ^6discord.gg/KMYkcdK")
        
    def cmd_help(self, data, client, cmd=None):
        fin = open("/home/urt4/urbanterror43/q3ut4/helpfile.txt", "rt")
        data = fin.read()
        data = data.replace('XDATA1', client.name)
        fin.close()
        fin = open("/home/urt4/urbanterror43/q3ut4/helpfile.txt", "wt")
        fin.write(data)
        fin.close()
        self.console.write('exec helpfile.txt')
        fin = open("/home/urt4/urbanterror43/q3ut4/helpfile.txt", "rt")
        data = fin.read()
        data = data.replace(client.name, 'XDATA1')
        fin.close()
        fin = open("/home/urt4/urbanterror43/q3ut4/helpfile.txt", "wt")
        fin.write(data)
        fin.close()

    def cmd_funremove(self, data, client, cmd=None):
        m = self._adminPlugin.parseUserCmd(data)
        if not m:
            client.message('^7!funremove <player>')
            return
        sclient = self._adminPlugin.findClientPrompt(m[0], client)
        if not sclient:
            return
        if client.maxLevel >= 20:
            self.console.write('forcecvar %s funred none' % sclient.name)
            self.console.write('forcecvar %s funblue none' % sclient.name)
            client.message('Removed funstuff from %s' % sclient.name)
        else:
            client.message('Insufficient rights')

    #def cmd_auth(self, data, client, cmd=None):
    #    last = client.var(self, 'delay_auth', 0).value
    #    if (self.console.time() - last) < 600:
    #        client.message('^3You can only use this command every 10 minutes')
    #    else:
    #        self.console.write('changeauth %s %s' % (client.cid, client.exactName))
    #        client.message('^5Auth ^3set ^2successfully!')
    #        client.setvar(self, 'delay_auth', self.console.time())

    def cmd_bhi(self, data, client, cmd=None):
        last = client.var(self, 'delay_hi', 0).value
        m = self._adminPlugin.parseUserCmd(data)
        if not m:
            client.message('^7!hi <player>')
            return

        sclient = self._adminPlugin.findClientPrompt(m[0], client)
        if not sclient:
            return
        
        if client.name == sclient.name:
            client.message('You can NOT say hi to yourself')
            return
     
        if (self.console.time() - last) < 120:
            client.message('^3You can only use this command every 2 minutes!')
        else:
            fin = open("/home/urt4/urbanterror43/q3ut4/hello.txt", "rt")
            data = fin.read()
            data = data.replace('player1', client.name)
            data = data.replace('player2', sclient.name)
            fin.close()
            fin = open("/home/urt4/urbanterror43/q3ut4/hello.txt", "wt")
            fin.write(data)
            fin.close()
            self.console.write('exec hello.txt')
            fin = open("/home/urt4/urbanterror43/q3ut4/hello.txt", "rt")
            data = fin.read()
            data = data.replace(client.name, 'player1')
            data = data.replace(sclient.name, 'player2')
            fin.close()
            fin = open("/home/urt4/urbanterror43/q3ut4/hello.txt", "wt")
            fin.write(data)
            fin.close()
            client.setvar(self, 'delay_bhi', self.console.time())

    def cmd_bhiall(self, data, client, cmd=None):
        last = client.var(self, 'delay_bhiall', 0).value
        if (self.console.time() - last) < 600:
            client.message('^3You can only use this command every 10 minutes')
        else:
            fin = open("/home/urt4/urbanterror43/q3ut4/hello2.txt", "rt")
            data = fin.read()
            data = data.replace('player', client.name)
            fin.close()
            fin = open("/home/urt4/urbanterror43/q3ut4/hello2.txt", "wt")
            fin.write(data)
            fin.close()
            self.console.write('exec hello2.txt')
            fin = open("/home/urt4/urbanterror43/q3ut4/hello2.txt", "rt")
            data = fin.read()
            data = data.replace(client.name, 'player')
            fin.close()
            fin = open("/home/urt4/urbanterror43/q3ut4/hello2.txt", "wt")
            fin.write(data)
            fin.close()
            client.setvar(self, 'delay_bhiall', self.console.time())

    def cmd_mapinfo(self, data, client, cmd=None):
        mapname = self.console.getMap()
        nextmapname = self.console.getNextMap()

        last = client.var(self, 'delay_mapinfo', 0).value
        if (self.console.time() - last) < 120:
            client.message('You can only use this command every 2 minutes')

        else:
            client.setvar(self, 'delay_mapinfo', self.console.time())
            fin = open("/home/urt4/urbanterror43/q3ut4/nmap.txt", "rt")
            data = fin.read()
            data = data.replace('xdata1', mapname)
            data = data.replace('xdata2', nextmapname)
            fin.close()
            fin = open("/home/urt4/urbanterror43/q3ut4/nmap.txt", "wt")
            fin.write(data)
            fin.close()
            self.console.write('exec nmap.txt')
            fin = open("/home/urt4/urbanterror43/q3ut4/nmap.txt", "rt")
            data = fin.read()
            data = data.replace(mapname, 'xdata1')
            data = data.replace(nextmapname, 'xdata2')
            fin.close()
            fin = open("/home/urt4/urbanterror43/q3ut4/nmap.txt", "wt")
            fin.write(data)
            fin.close()