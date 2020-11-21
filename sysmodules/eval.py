# -*- coding: utf-8 -*-
# Coded by @maxunof with power of Senko!

from meval import meval

import moduling
import utils


class Module(moduling.Module):
    def __init__(self, db):
        self.name = "Eval"
        self.db = db

    async def eval_cmd(self, client, message, cmd):
        if cmd.arg == "":
            await utils.send(message, '<b>You need to specify expression.</b>')
            return
        res = ""
        reply = None
        if message.is_reply:
            reply = (await message.get_reply_message())
        try:
            res = await meval(cmd.arg, globals(), db=self.db, client=client, message=message, cmd=cmd, reply=reply)
        except Exception as e:
            await utils.send(message, "<b>Can't eval expression:</b>\n<code>{}</code>\n\n<b>Source:</b>\n<code>{}</code>".format(utils.escape_html(str(e)), utils.escape_html(cmd.arg)))
            return
        await utils.send(message, "<b>Expression: </b><code>{}</code>\n<b>Result: </b><code>{}</code>".format(utils.escape_html(cmd.arg), utils.escape_html(str(res))))
