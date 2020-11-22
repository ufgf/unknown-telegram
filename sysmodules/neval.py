# -*- coding: utf-8 -*-
# Coded by @maxunof with power of Senko!

from meval import meval
from tinydb import where

import moduling
import utils


class Module(moduling.Module):
    def __init__(self, db):
        self.name = "Notes & Eval"
        self.db = db

    async def eval(self, client, message, cmd, expr):
        reply = None
        if message.is_reply:
            reply = (await message.get_reply_message())

        res = ""
        try:
            res = await meval(expr, globals(), db=self.db, client=client, message=message, cmd=cmd, reply=reply)
        except Exception as e:
            await utils.send(message, "<b>Can't eval expression:</b>\n<code>{}</code>\n\n<b>Source:</b>\n<code>{}</code>".format(utils.escape_html(str(e)), utils.escape_html(expr)))
            return
    
        await utils.send(message, "<b>Expression: </b><code>{}</code>\n<b>Result: </b><code>{}</code>".format(utils.escape_html(expr), utils.escape_html(str(res))))

    async def get_note(self, message, name):
        if name == "":
            await utils.send(message, "<b>You need to specify name of note</b>")
            return
        
        results = self.db.search(where("name") == name)
        if len(results) == 0:
            await utils.send(message, "<b>Note not found</b>")
            return

        return results[0]["value"]

    async def eval_cmd(self, client, message, cmd):
        if cmd.arg == "":
            await utils.send(message, "<b>You need to specify expression.</b>")
            return

        await self.eval(client, message, cmd, cmd.arg)        

    async def save_cmd(self, client, message, cmd):
        if not message.is_reply:
            await utils.send(message, "<b>You need to reply to the message</b>")
            return
        msg = (await message.get_reply_message())
        if msg.raw_text == "":
            await utils.send(message, "<b>Note is empty</b>")
            return
        if cmd.arg == "":
            await utils.send(message, "<b>You need to specify name of note</b>")
            return
        
        self.db.upsert({"name": cmd.arg, "value": {
            'raw': msg.raw_text,
            'text': msg.text
        }}, where("name") == cmd.arg)
        await utils.send(message, "<b>Note is saved</b>")

    async def note_cmd(self, client, message, cmd):
        note = await self.get_note(message, cmd.arg)
        if note is not None:
            await utils.send(message, note["text"])
    
    async def exec_cmd(self, client, message, cmd):
        note = await self.get_note(message, cmd.arg)
        if note is not None:
            await self.eval(client, message, cmd, note["raw"])
    
    async def notes_cmd(self, client, message, cmd):
        results = list("<code>{}</code>".format(utils.escape_html(x["name"])) for x in self.db)
        if len(results) == 0:
            await utils.send(message, "<b>You don't have any notes yet</b>")
            return
        
        await utils.send(message, "<b>List of notes:</b>\n" + ", ".join(results))

    async def delnote_cmd(self, client, message, cmd):
        if cmd.arg == "":
            await utils.send(message, "<b>You need to specify name of note</b>")
            return

        self.db.remove(where("name") == cmd.arg)
        await utils.send(message, "<b>Note deleted</b>")
