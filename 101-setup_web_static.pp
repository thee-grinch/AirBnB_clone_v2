# Configures web servers for the deployment of web_static using puppet
exec { 'apt_update':
  command     => '/usr/bin/apt-get update',
  path        => '/usr/bin',
  refreshonly => true,
}

package { 'nginx':
  ensure  => installed,
  require => Exec['apt_update'],
}

file { [
  '/data/',
  '/data/web_static/',
  '/data/web_static/releases/',
  '/data/web_static/releases',
  '/data/web_static/shared/',
  '/data/web_static/releases/test/',
]:
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

file { '/data/web_static/releases/test/index.html':
  content => '<h1>Hello from Testing</h1>',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
}

file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test/',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

exec { 'chown_web_static':
  command => '/bin/chown -R ubuntu:ubuntu /data/',
  path    => '/usr/bin',
  onlyif  => '/usr/bin/test ! -O /data/web_static/releases/test/index.html',
}

file { '/etc/nginx/sites-available/default':
  content => "
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name priscacreations.tech;

    add_header X-Served-B $(hostname);
    root /var/www/html/;
    index index.html index.htm index.nginx-debian.html;

    location /hbnb_static {
        alias /data/web_static/current/;
    }
    location /redirect_me {
        return 301 http://google.com/;
    }
    error_page 404 /404.html;
    location /404 {
        root /var/www/html;
        internal;
    }
}
",
  owner   => 'root',
  group   => 'root',
  mode    => '0644',
}

service { 'nginx':
  ensure  => running,
  enable  => true,
  require => [Package['nginx'], File['/etc/nginx/sites-available/default']],
}
