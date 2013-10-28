
from fabric.api import *
from deploy.core import *

import time
import functools


def tarball_from_jenkins(build_num, jenkins_server, jenkins_user, jenkins_key, name, tarball, prefix):
  build_url = '%s/job/%s/%s/artifact/build.tar.gz' % (jenkins_server, name, build_num)
  tmp_dir = '/tmp/prefixing-%s' % str(time.time())

  local('mkdir %s' % tmp_dir)

  with lcd(tmp_dir):
    local('curl -u %s:%s %s > %s' % (jenkins_user, jenkins_key, build_url, tarball))
    local('mkdir %s' % prefix)
    local('cd %s && tar -xzf ../%s' % (prefix, tarball))
    local('rm %s' % tarball)
    local('tar -czf %s %s' % (tarball, prefix))
    put(tarball)
  
  local('rm -rf %s' % tmp_dir)


@task
def app(name, build_num, jenkins_server, jenkins_user, jenkins_key, user='deploy', key='../keys/deploy', root='/var/app/'):
  app_dir = root + name + '/'

  wrap_deploy(
    str(time.time()), user, key,
    functools.partial(tarball_from_jenkins, build_num, jenkins_server, jenkins_user, jenkins_key, name),
    functools.partial(app_deploy, app_dir)
  )



