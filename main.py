# -*- coding: utf-8 -*-
# Coded by @maxunof with power of Senko!

import cmd
import importlib
import logging
import os
import subprocess
import sys

from git import Repo
from telethon.sync import TelegramClient, events
from tinydb import Query, TinyDB

import moduling
import utils

GIT_MASTER = "https://github.com/MaxUNof/unknown-telegram.git"

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(filename="utg.log", level=logging.INFO, filemode="w")
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

db = TinyDB('db.json')

logging.info("Loading modules...")

sys_modules = moduling.get_modules(moduling.get_modules_py("sysmodules"), db)
user_modules = moduling.get_modules(moduling.get_modules_py("modules"), db)
modules = sys_modules + user_modules

logging.info("Modules loaded: {}".format(len(modules)))

# TODO: Do this better
restart = False


async def helpcmd(client, message):
    sysmods = []
    usermods = []
    for mod in sys_modules:
        cmds = []
        for cmdname, _ in mod.commands.items():
            cmds.append(cmdname)
        sysmods.append(
            "<b>• {}:</b> <code>{}</code>".format(mod.name, ', '.join(cmds)))
    for mod in user_modules:
        cmds = []
        for cmdname, _ in mod.commands.items():
            cmds.append(cmdname)
        usermods.append(
            "<b>• {}:</b> <code>{}</code>".format(mod.name, ', '.join(cmds)))
    await utils.send(message, "<b>Help for Unknown Telegram</b>\n\n<b>System Modules:</b>\n{}\n\n<b>User Modules:</b>\n{}".format('\n'.join(sysmods), '\n'.join(usermods)))
    return True


async def updatecmd(client, message):
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
        return True
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
        return True
    if not 'master' in repo.heads:
        repo.create_head("master", origin.refs.master)
    repo.heads.master.set_tracking_branch(origin.refs.master)
    repo.heads.master.checkout(True)
    if hash == newhash:
        await utils.send(message, "<b>Already up to date!</b>")
        return True
    origin.pull()
    await utils.send(message, "<b>Updating requirements...</b>")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--user", "-r",
                        os.path.join(ROOT_DIR, "requirements.txt")])
    except subprocess.CalledProcessError:
        await utils.send(message, "<b>Can't update requirements!</b>")
        return True
    await utils.send(message, "<b>Update completed!</b>")
    global restart
    restart = True
    await client.disconnect()
    return True


async def restartcmd(client, message):
    await utils.send(message, "<b>Restarting...</b>")
    global restart
    restart = True
    await client.disconnect()
    return True


async def coreHandler(client, message, command):
    if command.cmd == "help":
        return (await helpcmd(client, message))
    if command.cmd == "update":
        return (await updatecmd(client, message))
    if command.cmd == "restart":
        return (await restartcmd(client, message))
    return False


async def outgoing_handler(event):
    client = event._client
    message = event.message
    command = cmd.Command(message.raw_text)
    if command.full == "":
        return
    if (await coreHandler(client, message, command)):
        return
    for module in modules:
        if command.cmd in module.commands:
            try:
                await module.commands[command.cmd](module.db, client, message, command)
            except Exception as e:
                logging.error(e)
                await utils.send(message, "<b>An error occurred while executing the module.</b>")
            break


async def incoming_handler(event):
    client = event._client
    message = event.message
    for module in modules:
        if module.incoming_handler is None:
            continue
        try:
            await module.incoming_handler(module.db, client, message)
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
client.add_event_handler(incoming_handler,
                         events.NewMessage(incoming=True))
client.add_event_handler(outgoing_handler,
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
