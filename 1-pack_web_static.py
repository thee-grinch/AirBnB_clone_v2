#!/usr/bin/python3
'''this module contains the function deploy'''
from datetime import datetime
from fabric import local
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
