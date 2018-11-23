# Created by: coderShan
# Created on: 2018/11/22
import os, re, tarfile
import types
from datetime import datetime
from inspect import isfunction

from fabric import Connection, config
from invoke import task

# 服务器MySQL用户名和口令:

db_user = 'root'
db_password = '3237383'
_TAR_FILE = 'dist-awesome.tar.gz'


@task
def hello(c):
    print("Hello Fabric")


@task
def build(c):
    # includes = ['static', 'templates', 'transwarp', 'favicon.ico', '*.py']
    # excludes = ['test', '.*', '*.pyc', "*.pyo"]
    c = Connection('65.49.215.135', user='root', port=27723, connect_kwargs={'password': 'ISIL60NlKphU'})
    # result = c.run('ls', hide=True)
    # msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
    # print(msg.format(result))
    c.local('cd %s' % os.path.join(os.path.abspath('.'), 'www'))
    c.local('del dist\\%s' % _TAR_FILE)
    tar = tarfile.open("dist\\%s" % _TAR_FILE, "w:gz")
    for root, _dir, files in os.walk("www/"):  # 打包www文件夹
        for f in files:
            if not (('.pyc' in f) or ('.pyo' in f)):  # 排除开发过程调试产生的文件，为了简单点实现，此处没有完全照搬廖老师的参数
                fullpath = os.path.join(root, f)
                tar.add(fullpath)
    tar.close()
    deploy(c)


_REMOTE_BASE_URL = '/root/python/blog'
_REMOTE_TMP_TAR = _REMOTE_BASE_URL + '/tmp/%s' % _TAR_FILE
_REMOTE_BASE_DIR = _REMOTE_BASE_URL + '/srv/awesome'


def deploy(c: Connection):
    newdir = 'www-%s' % datetime.now().strftime('%y-%m-%d_%H.%M.%S')
    c.run('rm -f %s' % _REMOTE_TMP_TAR)
    c.put('dist/%s' % _TAR_FILE, _REMOTE_TMP_TAR)
    with c.cd(_REMOTE_BASE_DIR):
        c.run('mkdir %s' % newdir)
    with c.cd("%s/%s" % (_REMOTE_BASE_DIR, newdir)):
        c.run('tar -xzvf %s --strip-components 1' % _REMOTE_TMP_TAR)
    with c.cd(_REMOTE_BASE_DIR):
        c.run('rm -f www')
        c.run('ln -s %s www' % newdir)
        c.run('chown root:root www')
        c.run('chown -R root:root %s' % newdir)
    c.config._config.__getitem__("run")['warn'] = True
    # c.run('supervisorctl stop awesome')
    # c.run('supervisorctl start awesome')
    c.run('supervisorctl shutdown')
    c.run('supervisord -c /etc/supervisor/supervisord.conf')
    c.run('/etc/init.d/nginx reload')
    c.config._config.__getitem__("run")['warn'] = False
