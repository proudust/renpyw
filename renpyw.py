#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Doki Doki Literature Club Mod Development Environment setup and build script.
"""
import glob
import hashlib
import os
import shutil
import subprocess
import sys

from renpyw_lib import fetch


def download_renpy_sdk():
    # type: () -> None
    """
    If "lib/renpy" does not exist, download Ren'Py SDK.
    """
    if not os.path.exists("lib/renpy"):
        fetch('https://www.renpy.org/dl/6.99.12.4/renpy-6.99.12.4-sdk.zip') \
            .unzip("lib/renpy", strip=1)


def apply_renpy_dialogue_patch():
    # type: () -> None
    """
    Downloads and apply Proudust's Extract Dialogue patch to Ren'Py
    """
    md5 = ''
    if os.path.exists('lib/renpy/renpy/translation/dialogue.py'):
        with open('lib/renpy/renpy/translation/dialogue.py', mode='rb') as f:
            md5 = hashlib.md5(f.read()).hexdigest()
    if md5 != '4cbb3233fff6d5d6e9bea3a7f5a10aa3':
        fetch('https://raw.githubusercontent.com/proudust/renpy/dialogue-patch/renpy/translation/dialogue.py') \
            .save('lib/renpy/renpy/translation/dialogue.py')


def download_ddlc():
    # type: () -> None
    """
    If "lib/ddlc" does not exist, download Ren'Py SDK.
    """
    if not os.path.exists("lib/ddlc"):
        url = fetch('https://teamsalvato.itch.io/ddlc/file/594897', "") \
            .as_json()["url"]
        fetch(url) \
            .unzip("lib/ddlc", strip=1)


def download_unrpyc():
    # type: () -> None
    """
    If "lib/unrpyc" does not exist, download unrpyc.
    """
    if not os.path.exists('lib/unrpyc'):
        fetch('https://github.com/CensoredUsername/unrpyc/archive/refs/heads/master.zip') \
            .unzip('lib/unrpyc', strip=1)


def download_mas(version):
    # type: (str) -> None
    """
    If "lib/mas_$version" does not exist, download Monika After Story.
    :param version: MAS version to download.
    """
    if not os.path.exists('lib/mas_' + version):
        shutil.copytree('lib/ddlc', 'lib/mas_' + version)
        url = fetch('https://api.github.com/repos/Monika-After-Story/MonikaModDev/releases/tags/' + version) \
            .as_json()['assets'][0]['browser_download_url']
        fetch(url) \
            .unzip('lib/mas_' + version + '/game')


def exec_unrpyc(source):
    if not glob.glob(source):
        subprocess.call([sys.executable, 'lib/unrpyc/unrpyc.py', '--clobber', source])


if __name__ == '__main__':
    download_renpy_sdk()
    apply_renpy_dialogue_patch()
    download_ddlc()
    download_unrpyc()
    download_mas('v0.12.4')
    exec_unrpyc("lib/mas_v0.12.4/game/*.rpyc")
