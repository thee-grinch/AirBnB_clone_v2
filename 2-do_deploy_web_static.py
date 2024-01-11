#!/usr/bin/python3
"""
Generates a .tgz archive using do_pack fun
"""
from fabric.api import local, run, put, env, task
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


@task
def do_deploy(archive_path):
    """Distributes an archive to the servers"""
    try:
        archive_filename = os.path.basename(archive_path)
        release_directory_name = archive_filename[:-4]

        put(archive_path, '/tmp/')
        run(f'mkdir -p /data/web_static/releases/{release_directory_name}/')
        run(f'tar -xzf /tmp/{archive_filename} -C /data/web_static/releases/\
            {release_directory_name}/')
        run(f'rm /tmp/{archive_filename}')

        run(f'mv /data/web_static/releases/{release_directory_name}\
             /web_static/* '
            f'/data/web_static/releases/{release_directory_name}/')

        run('rm -rf /data/web_static/releases/web_static')
        run('rm -rf /data/web_static/current')
        run(f'ln -s /data/web_static/releases/{release_directory_name}/ /data/\
             web_static/current')

        print("New version deployed!")
        return True
    except Exception:
        return False
