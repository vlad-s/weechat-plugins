# -*- coding: utf-8 -*-
# Copyright (c) 2014 by Vlad Stoica <stoica.vl@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# History
# 02-11-2014 - Vlad Stoica
# Initial script

import weechat as w

SCRIPT_NAME    = "auto_capital"
SCRIPT_AUTHOR  = "Vlad Stoica <stoica.vl@gmail.com>"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC    = "Politely writes your first word with a capital letter."

settings = {
        # we don't want to interfere with scripts' buffers
        "blacklist_buffers": ("scripts,iset", "Buffers to ignore"),
        }

# checks if a nickname exists on a buffer
def isnick(buff, nickname):
    return w.nicklist_search_nick(buff, "", nickname)

def word_magic(data, buffer, command):
    # get the input string
    uinput = w.buffer_get_string(buffer, "input")

    # if the buffer is blacklisted, do nothing
    if w.buffer_get_string(buffer, "short_name") in w.config_get_plugin(
            "blacklist_buffers").split(","):
        return w.WEECHAT_RC_OK

    if command == "/input return":
        # in case the line's empty, do nothing
        if uinput == "":
            return w.WEECHAT_RC_OK
        # bypass this using a backslash as the first character
        elif uinput.startswith("\\"):
            uinput = uinput.replace("\\", "", 1)
        # we don't want to capitalize basic URLs
        elif uinput[:4] == "http": # I'M TOO LAZY FOR REGEX MATCHING
            return w.WEECHAT_RC_OK
        # if we point to a user, don't capitalise this
        elif isnick(buffer, uinput.split()[0][:-1]):
            return w.WEECHAT_RC_OK
        # if everything else is fine, replace the first char with its capital
        else:
            uinput = uinput.replace(uinput[0], uinput[0].upper(), 1)
        # set the new string into the input
        w.buffer_set(buffer, "input", uinput)
    return w.WEECHAT_RC_OK

if w.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION,
        SCRIPT_LICENSE, SCRIPT_DESC, "", ""):
    for option, value in settings.items():
        if not w.config_is_set_plugin(option):
            w.config_set_plugin(option, value[0])
        w.config_set_desc_plugin(option, "%s (default '%s')" % (value[1],
            value[0]))
    w.hook_command_run("/input return", "word_magic", "")
