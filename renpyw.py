#!/usr/bin/env python

import io
import json
import os
import shutil
import urllib2
import zipfile


class HttpRequest(object):
    __slots__ = ['url', 'data', 'response']

    def __init__(self, url, data=None):
        self.url = url
        self.data = data
        self.response = None

    def as_bytesio(self):
        # type: () -> io.BytesIO
        if self.response is None:
            self.response = urllib2.urlopen(self.url, data=self.data)
        return io.BytesIO(self.response.read())

    def as_json(self):
        # type: () -> dict
        bytesio = self.as_bytesio()
        return json.load(bytesio)

    def as_zip(self):
        # type: () -> zipfile.ZipFile
        bytesio = self.as_bytesio()
        return zipfile.ZipFile(bytesio, "r")

    def as_zip_extract(self, dist):
        with self.as_zip() as archive:
            root_len = len(archive.namelist()[0].split('/')[0]) + 1
            for name in archive.namelist():
                if not name.endswith('/'):
                    source_path = name[root_len:]
                    dist_path = os.path.join(dist, source_path)
                    dist_dir = os.path.dirname(dist_path)
                    if not os.path.exists(dist_dir):
                        os.makedirs(dist_dir)

                    source_io = archive.open(name)
                    dist_io = open(dist_path, "wb")
                    with source_io, dist_io:
                        shutil.copyfileobj(source_io, dist_io)


def download_renpy_sdk():
    # type: () -> None
    """
    If "lib/renpy" does not exist , download Ren'Py SDK.
    """
    if not os.path.exists("lib/renpy"):
        HttpRequest('https://www.renpy.org/dl/6.99.12.4/renpy-6.99.12.4-sdk.zip') \
            .as_zip_extract("lib/renpy")


def download_ddlc():
    # type: () -> None
    """
    If "lib/ddlc" does not exist , download Ren'Py SDK.
    """
    if not os.path.exists("lib/ddlc"):
        url = HttpRequest('https://teamsalvato.itch.io/ddlc/file/594897', "") \
            .as_json()["url"]
        HttpRequest(url) \
            .as_zip_extract("lib/ddlc")


if __name__ == '__main__':
    download_renpy_sdk()
    download_ddlc()