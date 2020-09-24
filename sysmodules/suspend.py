# -*- coding: utf-8 -*-
# Coded by @maxunof with power of Senko!

import time

import moduling
import utils


class Module(moduling.Module):
    def __init__(self, db):
        self.name = "Suspension"

    async def suspend_cmd(self, client, message, cmd):
        try:
            seconds = int(cmd.arg)
            await utils.send(message, "<b>Bot is sleeping for {} seconds 😴</b>".format(seconds))
            time.sleep(seconds)
        except ValueError:
            await utils.send(message, "<b>Invalid suspension time.</b>")
