#!/usr/bin/python3
# this function deploys a function to a server
from fabric import put, run
import os


def do_deploy(archive_path):
    """this function deploys an archive to a web server"""
    if not os.path.exists(archive_path):
        return False
    try:
        put(archive_path, '/tmp/')
        file_name = archive_path.split('/')[1]
        file_without_ext = file_name.split('.')[0]
        run("tar -xcf /tmp/{} -C /data/web_static/releases/{}/".format(file_name, file_without_ext))
        run("rm /tmp/{}".format(file_name))
        run("rm  /data/web_static/current")
        run("ln -s /data/web_static/releases/{} /data/web_static/current".format(file_without_ext))
    except Exception:
        return False
    return True
