# Class: nrpe_monitoring
# Installs and configures Nagios Remote Plugin Executor (NRPE)
class nrpe_monitoring (
  $allowed_hosts = '127.0.0.1,::1,10.100.2.50'
) {
  package { ['nagios-nrpe-server', 'nagios-plugins']:
    ensure => installed,
  }

  file { '/etc/nagios/nrpe.cfg':
    ensure  => file,
    content => template('nrpe_monitoring/nrpe.cfg.erb'),
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    notify  => Service['nagios-nrpe-server'],
    require => Package['nagios-nrpe-server'],
  }

  service { 'nagios-nrpe-server':
    ensure => running,
    enable => true,
  }
}

