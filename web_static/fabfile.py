from fabric import Connection, task

CONNECTION_PROPERTIES = {
    'host': '54.88.227.197',
    'user': 'ubuntu',
    'connect_kwargs': {
        'key_filename': '/home/mordecai/.ssh/id_rsa'
    },
}

@task
def deploy(c):
    c = Connection(**CONNECTION_PROPERTIES)
    c.run('uname -a')
