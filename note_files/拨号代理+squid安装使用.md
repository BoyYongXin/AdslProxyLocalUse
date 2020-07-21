## conteos7 拨号代理配合squid安装使用

**安装 squid**

~~~
# rpm -qa | grep squid

squid-3.3.8-26.el7_2.4.x86_64       // 表示安装过

yum -y install squid               // 安装
~~~

 

**开机自启动 squid**

~~~
systemctl enable squid.service 
~~~

**配置 squid**

~~~
vi  /etc/squid/squid.conf
~~~

**修改如下几个部分**:

~~~
http_access allow !Safe_ports#deny改成allow

http_access allow CONNECT !SSL_ports#deny改成allow

http_access allow all#deny改成allow
~~~



**启动squid**

~~~
systemctl start squid.service
~~~

如果失败

## 可能出现的问题：

**问题一**

~~~
cd /etc/squid
[root @ localhost squid]  # squid -z 
squid: relocation error: squid: symbol SSL_set_alpn_protos, version
~~~

**参考链接**

 ~~~
https://blog.csdn.net/weixin_43557605/article/details/97238885

#解决步骤
yum -y install openssl openssl-devel
squid -z
squid
 ~~~

**问题 二**

~~~
[Squid启动报：Could not determine this machines public hostname. Please configure one or set 'visible_hostname'.](https://www.cnblogs.com/zd520pyx1314/p/9069067.html)
~~~

**参考链接**

~~~
https://www.cnblogs.com/zd520pyx1314/p/9069067.html
~~~

~~~
#解决步骤

在squid.conf中添加

visible_hostname squid.packet-pushers.net

或者编辑/etc/hosts文件，

在该文件中制定主机IP地址与主机名的对应.

squid -f /etc/squid/squid.conf

~~~

**最后查看是否配置成功**

~~~
#查看进程
ps -aef |grep squid
#查看端口
netstat -lnpt
~~~

