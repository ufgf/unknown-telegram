# -*- coding: utf-8 -*-
# Coded by @maxunof with power of Senko!

class Command():
    def __init__(self, text):
        self.full = ""
        self.cmd = ""
        self.arg = ""
        self.args = []
        if text.startswith("."):
            self.full = text[1:]
            split = self.full.split(" ", 1)
            self.cmd = split[0]
            if len(split) > 1:
                self.arg = split[1]
            self.args = self.arg.split(" ")
