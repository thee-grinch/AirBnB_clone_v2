#!/usr/bin/python3
'''this module contains the function deploy'''
from datetime import datetime
from fabric import local, run, put
import os


def do_pack():
    '''this function packs a directory into a .tgz file'''
    try:
        if not os.path.exists('versions'):
            os.makedirs('versions')
        date = datetime.now().strftime('%Y%m%d%H%M%S')
        file_name = "versions/web_static_{}.tgz".format(date)
        local('tar -cvzf {} web_static'.format(file_name))
        return file_name
    except:
        return None 

def do_deploy(archive_path):
    '''this function deploys an archive to a web server'''
    if not os.path.exists(archive_path):
        return False
    try:
        file_name = archive_path.split('/')[1]
        file_name_no_ext = file_name.split('.')[0]
        put(archive_path, '/tmp/')
        run('mkdir -p /data/web_static/releases/{}/'.format(file_name_no_ext))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(file_name, file_name_no_ext))
        run('rm /tmp/{}'.format(file_name))
        run('mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'.format(file_name_no_ext, file_name_no_ext))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(file_name_no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(file_name_no_ext))
        return True
    except:
        return False
