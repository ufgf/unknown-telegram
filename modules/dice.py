# -*- coding: utf-8 -*-
# Coded by @maxunof with power of Senko! 

from telethon.tl.types import InputMediaDice

import moduling
import utils


class Module(moduling.Module):
    def __init__(self, db):
        self.name = "Dice"

    async def dice_cmd(self, client, message, cmd):
        if len(cmd.args) == 0:
           await utils.send(message, "<b>Incorrect command usage!</b>\n<b>You can pass two arguments: number and emoji.</b>")
           return
        need = 0
        try:
            need = int(cmd.args[0])
        except:
            await utils.send(message, "<b>You need to specify the number that should fall out.</b>")
            return
        emoji = ""
        if len(cmd.args) > 1:
            emoji = cmd.args[1]
        await message.delete()
        count = 0
        while count != 15:
            msg = await client.send_file(message.chat_id, InputMediaDice(emoji))
            if msg.media.value == need:
                return
            await msg.delete()
            count = count+1
