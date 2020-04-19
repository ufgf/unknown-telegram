# -*- coding: utf-8 -*-
# Coded by @maxunof with power of Senko!

import moduling
import platform
import utils
import sys
import os
import time
from telethon import __version__
from git import Repo

class Module(moduling.Module):
    def __init__(self):
        self.name = "System Info"
        self.repo = Repo(os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__)))
        self.start = time.time()

    async def infocmd(self, db, client, message, cmd):
        os = platform.system()
        distr = ""
        if os == "Linux":
            with open("/etc/os-release") as f:
                for line in f:
                    k,v = line.rstrip().split("=")
                    if k != "NAME":
                        continue
                    distr = v.strip('"')
                    break
        commit = ""
        try:
            commit = self.repo.commit("master").__str__()[:10]
        except:
            pass
        pairs = {"OS": os, "Release": platform.release,
            "Distribution": distr,
            "Arch": platform.machine, "Python": platform.python_version,
            "Telethon": __version__, "Commit": commit,
            "Uptime": utils.formatSeconds(time.time() - self.start)}
        lines = []
        for name, item in pairs.items():
            res = ""
            if item.__class__.__name__ == "function":
                res = item()
            else:
                res = item
            if res:
                lines.append("<b>• {}</b>: <code>{}</code>".format(name, res))
        await utils.send(message, "<b>System Info:</b>\n" + '\n'.join(lines))
