yum -y install squid
yum -y install openssl openssl-devel

vi /etc/squid/squid.conf
#########
http_access allow !Safe_ports#deny改成allow
http_access allow CONNECT !SSL_ports#deny改成allow
http_access allow all#deny改成allow
visible_hostname squid.packet-pushers.net
#########

squid

systemctl enable squid.service
systemctl start squid.service
service squid reload
service squid restart

iptables -I INPUT -p tcp --dport 3128 -j ACCEPT

curl -x  61.131.227.180:3128 httpbin.org/get


/home/worker/yangyongxin

wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-6.repo

[root@localhost ~]# rm -rf /etc/yum.repo/*.repo
[root@localhost ~]# rpm -ivh epel-release-latest-7.noarch.rpm
[root@localhost ~]# yum clean all
[root@localhost ~]# yum makecache