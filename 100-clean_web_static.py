#!/usr/bin/python3
"""
Deletes out-of-date archives
"""
import os
from fabric.api import local, lcd, cd, run, env

env.hosts = ['52.201.221.134', '52.87.219.193']
env.user = 'ubuntu'

def do_clean(number=0):
    """Deletes out-of-date archives
    number: numbers of archives to keep"""
    if int(number) < 2:
        number = 1
    else:
        number = int(number)
    local_folder = './versions'
    with lcd(local_folder):
        local_archives = local('ls -t ', capture=True)
        to_delete_local = local_archives[number:] if local_archives else []

        for file in to_delete_local:
            local("rm -f {}".format(os.path.join(local_folder, file)))

    remote_folder = '/data/web_static/releases'
    with cd(remote_folder):
        remote_archives = run('ls -tr').split()
        remote_archives = [a for a in remote_archives if "web_static_" in a]
        to_delete_remote = remote_archives[number:]

        for archive in to_delete_remote:
            run('rm -rf {}'.format(os.path.join(remote_folder, archive)))
