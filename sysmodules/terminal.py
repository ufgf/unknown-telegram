# -*- coding: utf-8 -*-

import asyncio

import chardet
import moduling
import utils


class Module(moduling.Module):
    def __init__(self, db):
        self.name = "Terminal"

    async def run(self, message, cmd):
        sh = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE)
        await utils.send(message, "<b>Process is running...</b>")
        await sh.wait()

        out = (await sh.stdout.read())
        enc = chardet.detect(out)["encoding"]

        if enc is None:
            await utils.send(message, "<b>No data received</b>")
            return
        await utils.send(message, "<code>{}</code>".format(out.decode(enc)))

    async def neofetch_cmd(self, client, message, cmd):
        await self.run(message, "neofetch --stdout")

    async def terminal_cmd(self, client, message, cmd):
        await self.run(message, cmd.arg)
