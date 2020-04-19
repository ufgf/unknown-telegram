# -*- coding: utf-8 -*-
# Coded by @maxunof with power of Senko!

import moduling
import datetime
import utils

class Module(moduling.Module):
    def __init__(self):
        self.name = "Ping"

    async def pingcmd(self, db, client, message, cmd):
        start = datetime.datetime.now()
        await utils.send(message, "🏓 <b>Calculating...</b>")
        end = datetime.datetime.now()
        await utils.send(message, "🏓 Ping: <b>{}ms</b>".format((end - start).microseconds / 1000))

