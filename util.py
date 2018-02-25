import logging
import pathlib
import sys
from os.path import splitext
from urllib.parse import urlparse

from config import DATA_FOLDER


def g_path(*args):
    path = pathlib.Path(DATA_FOLDER, *args)
    path.parent.mkdir(exist_ok=True)
    return path


format = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=format)
logger = logging.getLogger("gakki_recognizer")


def get_extension(url):
    """Return the filename extension from url, or ''."""
    parsed = urlparse(url)
    root, ext = splitext(parsed.path)
    return ext
