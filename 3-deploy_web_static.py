#!/usr/bin/python3
"""
Fabric script based on the file 2-do_deploy_web_static.py that creates and
distributes an archive to the web servers

execute: fab -f 3-deploy_web_static.py deploy 
"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir

env.user = 'ubuntu'
env.hosts = ['100.25.165.125', '54.234.132.103']


def do_pack():
    """generates a tgz archive"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        file_new = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_new))
        return file_new
    except:
        return None


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


def deploy():
    """creates and distributes an archive to the web servers"""
    print("Executing task 'deploy'")
    archive_path = do_pack()
    if archive_path is None:
        return False
    print("New version deployed!")
    return do_deploy(archive_path)
