
from fabric.api import *

import time

env.user = 'deploy'

@task
def puppet(working_directory, user='deploy'):
  env.user = user

  with lcd(working_directory):
    local('git archive master | gzip > puppet.tar.gz')
    put('puppet.tar.gz')
    local('rm puppet.tar.gz')

  run('mkdir puppet')
  
  with cd('./puppet'):
    run('tar -xzf ../puppet.tar.gz')
    run('cp hiera.yaml hiera.yaml.orig')
    run('sed "s/\/vagrant\///g" hiera.yaml.orig > hiera.yaml')
    run('bundle install')
    run('bundle exec librarian-puppet install')
    sudo('bundle exec puppet apply --debug --verbose --summarize --reports store --hiera_config ./hiera.yaml --modulepath modules:vendor/modules --manifestdir manifests manifests/site.pp')

  run('rm -rf puppet')


@task
def static(name, wd, key='../keys/deploy', root='/var/www/'):
  env.key_filename = key
  env.sudo_prompt = ''
  env.sudo_prefix = 'sudo '

  tarball = name + '.deploy.tar.gz'
  app_dir = root + name + '/'
  deploy_dir = str(time.time())

  with lcd(wd):
    local('git archive master | gzip > ' + tarball)
    put(tarball)
    local('rm ' + tarball)

  sudo('mkdir "' + app_dir + deploy_dir + '"')
  sudo('cd "' + app_dir + deploy_dir + '" && tar -xzf /home/' + env.user + '/' + tarball)
  sudo('rm -f "' + app_dir + 'current"')
  sudo('ln -s "' + app_dir + deploy_dir + '" "' + app_dir + 'current"')

  run('rm ~/' + tarball)







