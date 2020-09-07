# -*- coding: utf-8 -*-

import subprocess

import moduling
import utils


class Module(moduling.Module):
    def __init__(self):
        self.name = "Neofetch"

    async def neofetch_cmd(self, db, client, message, cmd):
        await message.edit("<code>" + str(subprocess.check_output(["neofetch", "--stdout"]).decode("utf-8")) + "</code>")
