# Class: nginx_server
# Manages Nginx installation, web root configuration, and service state
class nginx_server {
  package { 'nginx':
    ensure => installed,
  }

  file { '/var/www/html/index.html':
    ensure  => file,
    content => template('nginx_server/index.html.erb'),
    owner   => 'www-data',
    group   => 'www-data',
    mode    => '0644',
    require => Package['nginx'],
  }

  service { 'nginx':
    ensure    => running,
    enable    => true,
    subscribe => File['/var/www/html/index.html'],
  }
}

