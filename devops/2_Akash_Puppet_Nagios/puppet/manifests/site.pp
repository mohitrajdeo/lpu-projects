# INT333: Centralized Puppet Catalog Definition (site.pp)
# Student: Akash Choudhary (12301625)

node default {
  include ssh_hardening
  include nrpe_monitoring
}

node 'agent1.devops.local' {
  include nginx_server
  include ssh_hardening
  include nrpe_monitoring
}

node 'agent2.devops.local' {
  include ssh_hardening
  include nrpe_monitoring
}

