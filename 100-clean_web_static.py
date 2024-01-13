#!/usr/bin/python3
"""
Deletes out-of-date archives
"""
import os
from datetime import datetime
from fabric.api import local, lcd, cd, run, put, env


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
        run("sudo rm -rf /data/web_static/current/")
        run("mkdir -p /data/web_static/current/")
        run("sudo ln -snf {} /data/web_static/current".format(target_folder))

        print("New version deployed!")
        return True

    return False


def deploy():
    """Deploys to servers"""

    path = do_pack()
    if path:
        return do_deploy(path)
    else:
        return False



def do_clean(number=0):
    """Deletes out-of-date archives
    number: numbers of archives to keep"""
    if int(number) < 2:
        number = 1
    else:
        number = int(number)
    local_folder = './versions'
    with lcd(local_folder):
        local_archives = local('ls -t | grep web_static', capture=True)
        to_delete_local = local_archives[number:] if local_archives else []

        for file in to_delete_local:
            local("rm -f {}".format(os.path.join(local_folder, file)))

    remote_folder = '/data/web_static/releases'
    with cd(remote_folder):
        remote_archives = run('ls -t | grep web_static').split('\n')
        to_delete_remote = remote_archives[number:]

        for archive in to_delete_remote:
            run('rm -f {}'.format(os.path.join(remote_folder, archive)))
