# Class: ssh_hardening
# Enforces enterprise SSH security baseline
class ssh_hardening {
  package { 'openssh-server':
    ensure => installed,
  }

  file { '/etc/ssh/sshd_config':
    ensure  => file,
    content => template('ssh_hardening/sshd_config.erb'),
    owner   => 'root',
    group   => 'root',
    mode    => '0600',
    notify  => Service['ssh'],
    require => Package['openssh-server'],
  }

  service { 'ssh':
    ensure => running,
    enable => true,
  }
}

