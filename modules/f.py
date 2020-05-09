# -*- coding: utf-8 -*-
# Coded by @maxunof with power of Senko! 

import moduling
import utils
import random
import emoji

class Module(moduling.Module):
    def __init__(self):
        self.name = "F"
        self.patterns = ["FFFFF\nF\nFFF\nF\nF"] # maybe will be expanded
        self.emoji_patterns = ["FFFF\nF\nFFF\nF\nF"]

    async def fcmd(self, db, client, message, cmd):
        symbol = ""
        res = ""
        if cmd.arg in emoji.UNICODE_EMOJI:
            symbol = cmd.arg
            res = random.choice(self.emoji_patterns)
        else:
            symbol = ('F' if len(cmd.arg) != 1 else cmd.arg)
            res = random.choice(self.patterns)
        if symbol != "F":
            res  = res.replace("F", symbol)
        await utils.send(message, "<code>{}</code>".format(res))