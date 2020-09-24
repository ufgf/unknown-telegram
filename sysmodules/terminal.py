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

        stdout = ""
        if enc is None:
            stdout = "No data received"
        else:
            stdout = out.decode(enc)

        await utils.send(message, "<b>Command: </b><code>{}</code>\n<b>Status code: </b><code>{}</code>\n\n<b>Output:</b>\n<code>{}</code>".format(utils.escape_html(cmd), sh.returncode, utils.escape_html(stdout)))

    async def neofetch_cmd(self, client, message, cmd):
        await self.run(message, "neofetch --stdout")

    async def terminal_cmd(self, client, message, cmd):
        await self.run(message, cmd.arg)
