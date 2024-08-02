#!/usr/bin/python3
"""In this module a Fabric script that generates a .tgz archive."""
fron fabric.api import *
import os
from datetime import datetime


def do_pack():
    """
    Archives the static files.

    Returns
    -------
    str
        The archive path if it's been correctly generated otherwise None
    """
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    # or local('sudo mkdir -p versions')
    d_time = datetime.now()
    time_str = d_time.strftime("%Y%m%d%H%M%S")
    file_path = "versions/web_static_{}.tgz".format(time_str)
    try:
        print("Packing web_static to {}".format(file_path))
        local("tar -cvzf {} web_static".format(file_path))
        file_size = os.path.getsize(file_path)
        print("web_static packed: {} -> {} Bytes".format(file_path, file_size))
    except Exception as e:
        file_path = None
    return file_path
