#!/usr/bin/python3
"""
Generates a .tgz archive using do_pack fun
"""
from fabric.api import local, run, put, env
from datetime import datetime
import os

env.hosts = ['52.201.221.134', '52.87.219.193']
env.user = 'ubuntu'


def do_pack():
    """Generates a .tgz archive"""
    try:
        date = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        archive_name = "web_static_{}.tgz".format(date)
        full_path = "versions/{}".format(archive_name)
        local("tar -cvzf {} web_static/".format(full_path))
        return full_path
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to web servers.
    """
    if os.path.exists(archive_path):
        archive_filename = os.path.basename(archive_path)
        target_folder = "/data/web_static/releases/{}".format(archive_filename
                                                              [:-4])
        temp_archive_path = "/tmp/{}".format(archive_filename)

        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(target_folder))
        run("sudo tar -xzvf {} -C {}/".format(temp_archive_path,
                                              target_folder))
        run("sudo rm {}".format(temp_archive_path))
        run("sudo mv {}/web_static/* {}".format(target_folder,
                                                target_folder))
        run("sudo rm -rf {}/web_static".format(target_folder))
        run("rm -f /data/web_static/current/")
        run("mkdir -p /data/web_static/current/")
        run("sudo ln -snf {} /data/web_static/current".format(target_folder))

        print("New version deployed!")
        return True

    return False
