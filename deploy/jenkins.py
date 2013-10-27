
from fabric.api import *

import time


@task
def app(name, build_num, jenkins_server, jenkins_user, jenkins_key, user='deploy', key='../keys/deploy', root='/var/app/'):
  env.user = user
  env.key_filename = key
  env.sudo_prompt = ''
  env.sudo_prefix = 'sudo '

  tarball = name + '.deploy.tar.gz'
  app_dir = root + name + '/'
  deploy_dir = str(time.time())

  build_url = '%s/job/%s/%s/artifact/build.tar.gz' % (jenkins_server, name, build_num)

  local('curl -u %s:%s %s > %s' % (jenkins_user, jenkins_key, build_url, tarball))
  put(tarball)
  local('rm %s' % tarball)

  sudo('mkdir -p %s%s' % (app_dir, deploy_dir))
  sudo('cd "%s%s" && tar -xzf /home/%s/%s' % (app_dir, deploy_dir, user, tarball))
  sudo('rm -f "%scurrent"' % (app_dir))
  sudo('ln -s "%s%s" "%scurrent"' % (app_dir, deploy_dir, app_dir))

  with settings(warn_only=True):
    sudo('stop %s' % name)
    sudo('start %s' % name)

  run('rm ~/%s' % tarball)
