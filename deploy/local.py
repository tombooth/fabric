
from fabric.api import *
from deploy.core import *

import time
import functools

def tarball_from_local(wd, name, prefix):
  with lcd(wd):
    local('git archive-all --prefix="' + prefix + '" %s' % name)
    put(name)
    local('rm %s' % name)
  
@task
def puppet(wd, user='deploy', key='../keys/deploy'):
  wrap_deploy(
    'puppet', user, key,
    functools.partial(tarball_from_local, wd),
    puppet_deploy
  )

@task
def static(name, wd, user='deploy', key='../keys/deploy', root='/var/www/'):
  app_dir = root + name + '/'

  wrap_deploy(
    str(time.time()), user, key,
    functools.partial(tarball_from_local, wd),
    functools.partial(simple_deploy, app_dir)
  )


@task
def app(name, wd, user='deploy', key='../keys/deploy', root='/var/app/'):
  app_dir = root + name + '/'

  wrap_deploy(
    str(time.time()), user, key,
    functools.partial(tarball_from_local, wd),
    functools.partial(app_deploy, app_dir)
  )









