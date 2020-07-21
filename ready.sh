yum -y install squid
yum -y install openssl openssl-devel
iptables -I INPUT -p tcp --dport 3128 -j ACCEPT
systemctl enable squid.service