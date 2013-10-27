
from fabric.api import *

import deploy
import deploy.jenkins
import deploy.local

@task
def bootstrap(hostname):
  env.user = 'root'

  run('echo "%s" > /etc/hostname' % hostname)
  run('cp /etc/hosts /etc/hosts.orig')
  run('sed "s/ubuntu/' + hostname + '/g" /etc/hosts.orig > /etc/hosts')

  run('sysctl -w net.ipv6.conf.all.disable_ipv6=1')
  run('echo "net.ipv6.conf.all.disable_ipv6=1" > /etc/sysctl.d/disableipv6.conf')

  run('apt-get update')
  run('apt-get install -y build-essential git ruby1.9.3')
  run('gem install --no-rdoc --no-ri bundler')

  run('shutdown -r now')

@task
def bootstrap_puppet(wd):
  deploy.puppet(wd, 'root')

