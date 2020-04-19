# -*- coding: utf-8 -*-
# Coded by @maxunof with power of Senko!

import importlib
import os
import sys
import logging
import moduling
import cmd
import subprocess
import utils
from telethon.sync import TelegramClient, events
from git import Repo
from tinydb import TinyDB, Query

GIT_MASTER = "https://github.com/MaxUNof/unknown-telegram.git"

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(filename="utg.log", level=logging.INFO, filemode="w")
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

db = TinyDB('db.json')

logging.info("Loading modules...")

sysModules = moduling.getModules(moduling.getModulesPy("sysmodules"), db)
userModules = moduling.getModules(moduling.getModulesPy("modules"), db)
modules = sysModules + userModules

logging.info("Modules loaded: {}".format(len(modules)))

restart = False

async def outgoingHandler(event):
    client = event._client
    message = event.message
    command = cmd.Command(message.raw_text)
    if command.full != "":
        global restart
        if command.cmd == "help":
            sysmods = []
            usermods = []
            for mod in sysModules:
                cmds = []
                for cmdname, _ in mod.commands.items():
                    cmds.append(cmdname)
                sysmods.append(
                    "<b>• {}:</b> <code>{}</code>".format(mod.name, ', '.join(cmds)))
            for mod in userModules:
                cmds = []
                for cmdname, _ in mod.commands.items():
                    cmds.append(cmdname)
                usermods.append(
                    "<b>• {}:</b> <code>{}</code>".format(mod.name, ', '.join(cmds)))
            await utils.send(message, "<b>Help for Unknown Telegram</b>\n\n<b>System Modules:</b>\n{}\n\n<b>User Modules:</b>\n{}".format('\n'.join(sysmods), '\n'.join(usermods)))
            return
        if command.cmd == "update":
            await utils.send(message, "<b>Fetching last version from the git...</b>")
            repo = Repo(ROOT_DIR)
            try:
                origin = repo.remotes['origin']
                repo.delete_remote(origin)
            except:
                pass
            try:
                origin = repo.create_remote('origin', GIT_MASTER)
            except:
                await utils.send(message, "<b>Can't recreate origin!</b>")
                return
            hash = ""
            newhash = ""
            try:
                hash = repo.commit("master").__str__()
            except:
                pass
            try:
                fetch = origin.fetch()
                newhash = fetch[0].commit.__str__()
            except:
                await utils.send(message, "<b>Invalid git credentials!</b>")
                return
            if not 'master' in repo.heads:
                repo.create_head("master", origin.refs.master)
            repo.heads.master.set_tracking_branch(origin.refs.master)
            repo.heads.master.checkout(True)
            if hash == newhash:
                await utils.send(message, "<b>Already up to date!</b>")
                return
            origin.pull()
            await utils.send(message, "<b>Updating requirements...</b>")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "--user", "-r",
                    os.path.join(ROOT_DIR, "requirements.txt")])
            except subprocess.CalledProcessError:
                await utils.send(message, "<b>Can't update requirements!</b>")
                return
            await utils.send(message, "<b>Update completed!</b>")
            restart = True
            await client.disconnect()
            return
        if command.cmd == "restart":
            await utils.send(message, "<b>Restarting...</b>")
            restart = True
            await client.disconnect()
            return
        for module in modules:
            if command.cmd in module.commands:
                try:
                    await module.commands[command.cmd](module.db, client, message, command)
                except Exception as e:
                    logging.error(e)
                    await utils.send(message, "<b>An error occurred while executing the module.</b>")
                break

async def incomingHandler(event):
    client = event._client
    message = event.message
    for module in modules:
        if module.incomingHandler is not None:
            try:
                await module.incomingHandler(module.db, client, message)
            except Exception as e:
                logging.error(e)

client = TelegramClient(
    'utg',
    api_id=6,
    api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e",
    app_version="6.0.1 (19117)",
    device_model="OnePlusONEPLUS A5010",
    system_version="SDK 29")
client.parse_mode = "html"
client.start(lambda: input('Please enter your phone: '))
client.add_event_handler(incomingHandler,
    events.NewMessage(incoming=True))
client.add_event_handler(outgoingHandler,
    events.NewMessage(outgoing=True, forwards=False))
client.run_until_disconnected()

if restart:
    logging.info("Restarting...")
    python = sys.executable
    if sys.platform == 'win32':
        cmd = [python] + sys.argv
        cmd = subprocess.list2cmdline(cmd)
        sts = os.spawnv(os.P_WAIT, python, [cmd])
        os._exit(sts)
    else:
        os.execl(python, python, *sys.argv)