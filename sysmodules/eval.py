# -*- coding: utf-8 -*-
# Coded by @maxunof with power of Senko!

import moduling
import utils
from meval import meval


class Module(moduling.Module):
    def __init__(self):
        self.name = "Eval"

    async def evalcmd(self, db, client, message, cmd):
        if cmd.arg == "":
            await utils.send(message, '<b>You need to specify expression.</b>')
            return
        res = ""
        try:
            res = await meval(cmd.arg, globals())
        except Exception as e:
            await utils.send(message, "<b>Can't eval expression:</b>\n<code>{}</code>".format(e))
            return
        await utils.send(message, "<b>Expression: </b><code>{}</code>\n<b>Result: </b><code>{}</code>".format(cmd.arg, str(res)))
