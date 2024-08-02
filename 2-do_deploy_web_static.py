#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers
The sript takes the following steps:
    Upload the archive to the /tmp/ directory of the web server.
    Uncompress the archive to the folder
    /data/web_static/releases/<archive filename without extension>
    on the web server.
    Delete the archive from the web server.
    Delete the symbolic link /data/web_static/current from the web server.
    Create a new the symbolic link /data/web_static/current on the web server,
    linked to the new version of your code
    (/data/web_static/releases/<archive filename without extension>).

execute fab -f 2-do_deploy_web_static.py do_deploy -i ~/.ssh/id_rsa -u ubuntu
"""

from datetime import datetime
from fabric.api import *
import os

env.hosts = ["100.25.161.249", "54.162.44.141"]
env.user = "ubuntu"


def do_pack():
    """
    Create archive locally

    Returns
    -------
    str:
        Archive path if archive has generated correctly otherwise None.
    """
    date_str = datetime.now().strftime("%Y%m%d%H%M%S")
    # create a directory versions
    local("mkdir -p versions")
    archived_f_path = "versions/web_static_{}.tgz".format(date_str)
    # create the archive
    t_gzip_archive = local("tar -cvzf {} web_static".format(archived_f_path))
    if t_gzip_archive.succeeded:
        return archived_f_path
    else:
        return None


def do_deploy(archive_path):
    """
    Distribute archive to web servers

    Parameters
    ----------
    archive_path : str
        Path of archive file to distribute

    Returns
    -------
    bool:
        True if all operations have been done correctly, otherwise False.
    """
    if os.path.exists(archive_path) is False:
        return False
    try:
        archived_file = archived_path.split("/")[-1]
        no_extension = archived_file.split(".")[0]
        new_archive_path = f"/data/web_static/releases/{no_extension}"
        archived_file = "/tmp/" + archived_file
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(new_archive_path))
        run("sudo tar -xzf {} -C {}/".format(archived_file, new_archive_path))
        run("sudo rm {}".format(archived_file))
        run("sudo mv {}/web_static/* {}".format(new_archive_path,
                                                new_archive_path))
        run("sudo rm -rf {}/web_static".format(new_archive_path))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(new_archive_path))
        print("New version deployed!")
        return True
    except Exception as e:
        return False
