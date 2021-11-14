# -*- coding: utf-8 -*-
import io
import json
import os
import shutil
import urllib2
import zipfile


def fetch(url, data=None):
    # type: (str, any) -> FetchResponse
    """
    Fetching a resource from the network.
    :param url: URL of the resource you want to fetch.
    :param data: Any body that you want to add to your request.
    :return: Response to a request.
    """
    response = urllib2.urlopen(url, data=data)
    return FetchResponse(response.read())


class FetchResponse(object):
    """
    Response to a fetch request.
    """

    __slots__ = ['response']

    def __init__(self, response):
        self.response = response

    def as_bytesio(self):
        # type: () -> io.BytesIO
        """
        Get this response as io.BytesIO.
        :return: Response as io.BytesIO.
        """
        return io.BytesIO(self.response)

    def as_json(self):
        # type: () -> dict
        """
        Deserialize this response as json and return directory.
        :return: Dictionary deserialized from response as json.
        """
        bytesio = self.as_bytesio()
        return json.load(bytesio)

    def as_zip(self):
        # type: () -> zipfile.ZipFile
        """
        Get this response as zipfile.ZipFile.
        :return: Response as zipfile.ZipFile.
        """
        bytesio = self.as_bytesio()
        return zipfile.ZipFile(bytesio, "r")

    def save(self, dist):
        # type: (str) -> None
        """
        Save this response to the destination path.
        :param dist: Path to save this response.
        """
        content = self.as_bytesio().read()
        with open(dist, mode='wb') as f:
            f.write(content)

    def unzip(self, dist, strip=0):
        # type: (str, int) -> None
        """
        Unzip the response as a zip.
        :param dist: Save destination of the extracted files.
        :param strip: strip leading directory from file names on extraction.
        """
        with self.as_zip() as archive:
            for source_path in archive.namelist():
                if not source_path.endswith('/'):
                    stripped_path = '/'.join(source_path.split('/')[strip:])
                    dist_path = os.path.join(dist, stripped_path)
                    dist_dir = os.path.dirname(dist_path)
                    if not os.path.exists(dist_dir):
                        os.makedirs(dist_dir)

                    source_io = archive.open(source_path)
                    dist_io = open(dist_path, "wb")
                    with source_io, dist_io:
                        shutil.copyfileobj(source_io, dist_io)
