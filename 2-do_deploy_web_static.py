#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import put, run, env
from os.path import exists

env.user = 'ubuntu'
env.hosts = ['54.157.188.26', '54.175.132.69']


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_new = archive_path.split("/")[-1]
        ext = file_new.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_new, path, ext))
        run('rm /tmp/{}'.format(file_new))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, ext))
        run('rm -rf {}{}/web_static'.format(path, ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, ext))
        return True
    except:
        return False
