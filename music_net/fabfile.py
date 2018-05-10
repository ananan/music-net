from fabric.api import run, env, local, put

env.user = 'root'
env.host = '112.74.46.34'


def pack():
    local("tar czvf app.tar.gz ./* --exclude='*.tar.gz'")


def deploy():
    put('app.tar.gz', '/tmp/app.tar.gz')

