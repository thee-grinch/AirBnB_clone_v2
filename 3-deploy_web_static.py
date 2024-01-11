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
    """Distributes an archive to your web servers"""
    if not os.path.exists(archive_path):
        return False
    try:
        put(archive_path, "/tmp/")
        archive_filename = os.path.basename(archive_path)
        folder = "/data/web_static/releases/{}".format(archive_filename.split('.')[0])
        run("sudo mkdir -p {}".format(folder))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, folder))
        run("sudo rm /tmp/{}".format(archive_filename))
        current_link = "/data/web_static/current"
        run("sudo rm -rf {}".format(current_link))
        run("sudo ln -s {} {}".format(folder, current_link))
        print("New version deployed!")
        return True
    except Exception as e:
        print(e)
        return False


def deploy():
    """Deploys to servers"""

    path = do_pack()
    if path:
        return do_deploy(path)
    else:
        return False
