"""Utility functions for the csdmpy module."""
import sys
from os import path
from urllib.parse import quote
from urllib.parse import urlparse

import requests


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
__all__ = ["parse_url", "download_file_from_url"]


def parse_url(url):
    """Parse url"""
    res = urlparse(quote(url, safe="/?#@:"))
    return res


def download_file_from_url(url, verbose=False):
    """Download file from url"""
    res = parse_url(url)
    filename = path.split(res[2])[1]
    if path.isfile(filename):
        if verbose:
            sys.stdout.write(
                f"Found a local file with the filename, {0}. Skipping download."
            )
        return filename

    with open(filename, "wb") as file:
        response = requests.get(url, stream=True)
        total = response.headers.get("content-length")

        if total is None:
            file.write(response.content)
        else:
            downloaded = 0
            total = int(total)
            if verbose:
                sys.stdout.write(
                    "Downloading '{}' from '{}' to file '{}'.\n".format(
                        res[2], res[1], filename
                    )
                )
            for data in response.iter_content(
                chunk_size=max(int(total / 1000), 1024 * 1024)
            ):
                downloaded += len(data)
                file.write(data)
                if verbose:
                    done = int(20 * downloaded / total)
                    sys.stdout.write("\r[{}{}]".format("█" * done, "." * (20 - done)))
                    sys.stdout.flush()
    if verbose:
        sys.stdout.write("\n")

    return filename


def _get_absolute_data_address(data_path, file):
    """Return the absolute path address of a local data file.

    :params: data_path:
    """
    _file_abs_path = path.abspath(file)
    _path, _file = path.split(_file_abs_path)
    _join = path.join(_path, data_path)
    _join = path.normpath(_join)
    return "file:" + _join


def get_absolute_url_path(url, file):
    """Return absolute path to url"""
    res = parse_url(url)
    url_path = res.geturl()
    if res.scheme in ["file", ""]:
        if res.netloc == "":
            url_path = _get_absolute_data_address(res.path, file)
    return url_path


def get_relative_url_path(dataset_index, filename):
    """Return relative path to url"""
    index = str(dataset_index)
    absolute_path = get_absolute_url_path("", filename)

    name = path.splitext(path.split(filename)[1])[0] + "_" + index + ".dat"

    relative_url_path = path.join("file:.", name)

    absolute_path = path.abspath(
        urlparse(path.join(absolute_path, urlparse(relative_url_path).path)).path
    )
    return relative_url_path, absolute_path
