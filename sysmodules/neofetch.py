# -*- coding: utf-8 -*-

import moduling
import utils
import subprocess
class Module(moduling.Module):
    def __init__(self):
        self.name = "Neofetch"

    async def neofetchcmd(self, db, client, message, cmd):
        await message.edit("<code>" + str(subprocess.check_output(["neofetch", "--stdout"]).decode("utf-8"))  +  "</code>")
