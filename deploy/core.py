
from fabric.api import *

import json

def wrap_deploy(prefix, user, key, put_tarball, deploy):
  env.user = user
  env.key_filename = key
  env.sudo_prompt = ''
  env.sudo_prefix = 'sudo '

  tarball = 'deploy.tar.gz'

  put_tarball(tarball, prefix)

  deploy(tarball, prefix)

  run('rm ~/%s' % tarball)


def puppet_deploy(environment_yaml, tarball, prefix):
  run('tar -xzf %s' % tarball)

  with cd('./%s' % prefix):
    run('cp hiera.yaml hiera.yaml.orig')
    run('sed "s/\/vagrant\///g" hiera.yaml.orig > hiera.yaml')

    if environment_yaml is not None:
        put(environment_yaml, './hieradata/environment.yaml')

    run('bundle install')
    run('bundle exec librarian-puppet install')
    sudo('bundle exec puppet apply --debug --verbose --summarize --reports store --hiera_config ./hiera.yaml --modulepath modules:vendor/modules --manifestdir manifests manifests/site.pp')

  run('rm -rf %s' % prefix)


def simple_deploy(app_dir, tarball, prefix):
  sudo('cd "%s" && tar -xzf /home/%s/%s' % (app_dir, env.user, tarball))
  sudo('rm -f "%scurrent"' % (app_dir))
  sudo('ln -s "%s%s" "%scurrent"' % (app_dir, prefix, app_dir))


def app_deploy(app_dir, tarball, prefix):
  sudo('cd "%s" && tar -xzf /home/%s/%s' % (app_dir, env.user, tarball))

  descriptor_json = sudo('cat %sdescriptor.json' % app_dir)
  descriptor = json.loads(descriptor_json)

  if len(descriptor['post_deploy']) > 0:
    with cd('%s%s' % (app_dir, prefix)):
      for script in descriptor['post_deploy']:
        sudo(script)

  sudo('rm -f "%scurrent"' % (app_dir))
  sudo('ln -s "%s%s" "%scurrent"' % (app_dir, prefix, app_dir))

  if len(descriptor['services']) > 0:
    for service in descriptor['services']:
      with settings(warn_only=True):
        sudo('stop %s' % service)
        sudo('start %s' % service)

