# -*- coding: utf-8 -*-
# Coded by @maxunof with power of Senko!

import time
import tinydb

from telethon.tl.types import InputPeerUser

import moduling
import utils


def init_db(db):
    if len(db.all()) != 1:
        try:
            db.truncate()
        except:
            db.purge() # temporary
        db.insert({"afk": False, "note": "", "know": [], "since": 0})


class Module(moduling.Module):
    def __init__(self, db: tinydb.database.Table):
        self.name = "AFK"
        self.db = db

    async def afk_cmd(self, client, message, cmd):
        init_db(self.db)
        item = self.db.all()[0]
        if not item["afk"]:
            self.db.update({"afk": True, "note": cmd.arg,
                       "know": [], "since": time.time()})
            await utils.send(message, "<b>I'm going AFK</b>" + (('\n<b>Note: </b>' + cmd.arg) if cmd.arg else ""))
        else:
            await utils.send(message, "<b>I'm already AFK</b>" + (('\n<b>Note: </b>' + item["note"]) if item["note"] else ""))

    async def unafk_cmd(self, client, message, cmd):
        init_db(self.db)
        item = self.db.all()[0]
        if not item["afk"]:
            await utils.send(message, "<b>I haven't been AFK</b>")
        else:
            self.db.update({"afk": False, "note": "", "know": [], "since": 0})
            await utils.send(message, "<b>I'm no longer AFK</b>\n<b>Time spent in AFK: </b><i>{}</i>".format(utils.format_seconds(time.time() - item["since"])))

    async def incoming(self, client, message):
        if isinstance(message._input_chat, InputPeerUser):
            if not message._sender is None:
                if message._sender.bot:
                    return
            init_db(self.db)
            item = self.db.all()[0]
            if message.from_id in item["know"] or not item["afk"]:
                return
            if item["note"] != "":
                await utils.send(message, "<b>I'm AFK for</b> <i>{}</i><b>!</b>\n<b>Note: </b>{}".format(utils.format_seconds(time.time() - item["since"]), item["note"]))
            else:
                await utils.send(message, "<b>I'm AFK for</b> <i>{}</i><b>!</b>".format(utils.format_seconds(time.time()-item["since"])))
            self.db.update({"know": item["know"] + [message.from_id]})
