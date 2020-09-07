# -*- coding: utf-8 -*-
# Coded by @maxunof with power of Senko!

import moduling
import utils


class Module(moduling.Module):
    def __init__(self):
        self.name = "Dump"

    async def dump_cmd(self, db, client, message, cmd):
        msg = message
        if message.is_reply:
            msg = (await message.get_reply_message())
        await utils.send(message, "<code>{}</code>".format(msg.__str__()))
