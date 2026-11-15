#!/usr/bin/env bash
set -e

export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y autoconf gcc libc6 make wget unzip apache2 apache2-utils php libgd-dev libssl-dev libmcrypt-dev bc gawk dc build-essential snmp libnet-snmp-perl gettext

# 1. Create Nagios User and Group
useradd nagios || true
groupadd nagcmd || true
usermod -a -G nagcmd nagios
usermod -a -G nagcmd www-data

# 2. Download and Compile Nagios Core 4.5.2
cd /tmp
wget -O nagioscore.tar.gz https://github.com/NagiosEnterprises/nagioscore/archive/nagios-4.5.2.tar.gz
tar xzf nagioscore.tar.gz
cd nagioscore-nagios-4.5.2/

./configure --with-httpd-conf=/etc/apache2/sites-enabled
make all
make install-groups-users
usermod -a -G nagios www-data
make install
make install-daemoninit
make install-commandmode
make install-config
make install-webconf

# 3. Enable Apache Modules & Configure Web Password
a2enmod rewrite cgi
htpasswd -b -c /usr/local/nagios/etc/htpasswd.users nagiosadmin int333devopspassword
systemctl restart apache2

# 4. Download and Compile Nagios Plugins
cd /tmp
wget --no-check-certificate -O nagios-plugins.tar.gz https://github.com/nagios-plugins/nagios-plugins/releases/download/release-2.4.8/nagios-plugins-2.4.8.tar.gz
tar xzf nagios-plugins.tar.gz
cd nagios-plugins-2.4.8/
./configure --with-nagios-user=nagios --with-nagios-group=nagios
make
make install

# 5. Author Custom Dual-Tier Monitoring Configuration
cat << 'EOF' > /usr/local/nagios/etc/objects/devops_mohit.cfg
define host {
    use                     linux-server
    host_name               web-portal-server
    alias                   Mohit Web Portal & Code Runner Node
    address                 ${monitored_target_ip}
    max_check_attempts      5
    check_period            24x7
    notification_interval   30
    notification_period     24x7
}

# Tier 1: Ingress Web Portal Uptime (HTTP Port 80)
define service {
    use                     generic-service
    host_name               web-portal-server
    service_description     HTTP_Web_Portal_Uptime
    check_command           check_http!-u /health -e "healthy"
    check_interval          1
    retry_interval          1
    max_check_attempts      3
    notification_interval   15
}

# Tier 2: Backend Code Execution Engine Socket (TCP Port 9010)
define service {
    use                     generic-service
    host_name               web-portal-server
    service_description     TCP_Code_Execution_Engine
    check_command           check_tcp!9010
    check_interval          1
    retry_interval          1
    max_check_attempts      3
    notification_interval   15
}

# Tier 3: Host ICMP Ping Latency
define service {
    use                     generic-service
    host_name               web-portal-server
    service_description     ICMP_Ping_Host_Latency
    check_command           check_ping!100.0,20%!500.0,60%
    check_interval          1
    retry_interval          1
    max_check_attempts      5
}
EOF

# Include devops_mohit.cfg in nagios.cfg
echo "cfg_file=/usr/local/nagios/etc/objects/devops_mohit.cfg" >> /usr/local/nagios/etc/nagios.cfg

# Test and start Nagios
/usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg
systemctl enable nagios
systemctl start nagios

