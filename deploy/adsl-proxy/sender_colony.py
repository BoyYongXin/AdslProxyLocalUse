# !/usr/bin/env python
# -*-coding=utf-8 -*-
from multiprocessing.dummy import Pool as ThreadPool
import re
import requests
import paramiko
from requests.exceptions import ConnectionError, ReadTimeout
from loguru import logger
import time
from retrying import retry, RetryError
import redis
from db import RedisClient
import settings as settings

adsl_servers = settings.ADSL_SERVERS
PROXY_PORT = settings.PROXY_PORT
TEST_URL = settings.TEST_URL
TEST_TIMEOUT = settings.TEST_TIMEOUT
DIAL_CYCLE = settings.DIAL_CYCLE

class Monitor(object):
    def __init__(self, server_ip, port, user, pwd):
        """ 初始化ssh客户端 """
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client = client
            logger.info('------------开始连接服务器(%s)-----------' % server_ip)
            self.client.connect(server_ip, port, username=user, password=pwd, timeout=4)
            logger.info('------------认证成功!.....-----------')
        except Exception:
            logger.error('连接远程linux服务器(ip:{server_ip})发生异常!请检查用户名和密码是否正确!')

    def link_server(self, cmd):
        """连接服务器发送命令"""
        try:
            stdin, stdout, stderr = self.client.exec_command(cmd)
            content = stdout.read().decode('utf-8')
            return content
        except Exception as e:
            logger.error('link_server-->返回命令发生异常,内容:', e)
            self.client.close()

    def close_net(self):
        try:
            self.client.close()
        except Exception as e:
            logger.error("关闭连接error", e)


class Sender(object):
    """
    拨号并发送到 Redis
    """
    def __init__(self, server_ip, port, user, pwd, clent_name):
        self.CLIENT_NAME = clent_name
        self.ADSLHOST = server_ip
        self.ADSLPORT = port
        self.ADSLUSER = user
        self.ADSLPWD = pwd

    def test_proxy(self, proxy):
        """
        测试代理，返回测试结果
        :param proxy: 代理
        :return: 测试结果
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
            }
            response = requests.get(TEST_URL, proxies={
                'http': 'http://' + proxy,
                'https': 'https://' + proxy,
                # 'http': proxy,
                # 'https': proxy
            }, timeout=TEST_TIMEOUT,headers=headers,verify=False)
            if response.status_code == 200:
                return True
            else:
                return False
        except (ConnectionError, ReadTimeout):
            return False

    def parseIfconfig(self, data):
        data = data.split('\n\n')
        data = [i for i in data if i and i.startswith('ppp0')]
        ip = ""
        for line in data:
            re_ipaddr = re.compile(r'inet ([\d\.]{7,15})', re.M)
            ip = re_ipaddr.search(line)
            if ip:
                ip = ip.group(1)
            else:
                ip = ''
        return ip

    @retry(retry_on_result=lambda x: x is not True, stop_max_attempt_number=10)
    def remove_proxy(self):
        """
        移除代理
        :return: None
        """
        logger.info(f'Removing {self.CLIENT_NAME}...')
        try:
            # 由于拨号就会中断连接，所以每次都要重新建立连接
            if hasattr(self, 'redis') and self.redis:
                self.redis.close()
            self.redis = RedisClient()
            self.redis.remove(self.CLIENT_NAME)
            logger.info(f'Removed {self.CLIENT_NAME} successfully')
            return True
        except redis.ConnectionError:
            logger.info(f'Remove {self.CLIENT_NAME} failed')

    def set_proxy(self, proxy):
        """
        设置代理
        :param proxy: 代理
        :return: None
        """
        self.redis = RedisClient()
        if self.redis.set(self.CLIENT_NAME, proxy):
            logger.info(f'Successfully set proxy {proxy}')

    def loop(self):
        """
        循环拨号
        :return:
        """
        while True:
            logger.info('Starting dial...')
            self.run()
            time.sleep(DIAL_CYCLE)

    def run(self):
        """
        拨号主进程
        :return: None
        """
        logger.info('Dial started, remove proxy')
        try:
            self.remove_proxy()
        except RetryError:
            logger.error('Retried for max times, continue')
        # 拨号
        m = Monitor(self.ADSLHOST, self.ADSLPORT, self.ADSLUSER, self.ADSLPWD)
        m.link_server("adsl-stop")
        m.link_server("adsl-start")
        content = m.link_server("ifconfig")
        m.close_net()
        ip = self.parseIfconfig(content)
        if ip:
            proxy = "%s:%s" % (ip, PROXY_PORT)
            if self.test_proxy(proxy):
                logger.info(f'Valid proxy {proxy}')
                # 将代理放入数据库
                self.set_proxy(proxy)
                time.sleep(2)
                return True
            else:
                logger.error(f'Proxy invalid {proxy}')
                return False
        else:
            # 获取 IP 失败，重新拨号
            logger.error('Get IP failed, re-dialing')
            self.run()


def send(servers, loop=False):
    clent_name = servers["CLIENT_NAME"]
    server_ip = servers["ADSLHOST"]
    port = servers["ADSLPORT"]
    user = servers["ADSLUSER"]
    pwd = servers["ADSLPWD"]
    try:
        sender = Sender(server_ip, port, user, pwd, clent_name)
        sender.loop() if loop else sender.run()
        return True
    except Exception as err:
        logger.debug("send start error {}".format(err))
        return False

def main():
    pool = ThreadPool(38)
    results = pool.map(send, adsl_servers)  # 该语句将不同的url传给各自的线程，并把执行后结果返回到results中
    success = results.count(True)
    faild = results.count(False)
    logger.info(
        '''
        共导入ip到redis成功%s条
        共导入ip到redis失败%s条
       '''
        % (success, faild))
    pool.close()
    pool.join()

if __name__ == '__main__':
    main()
    # while True:
    #     logger.info('Starting dial...')
    #     main()
        # squid_keeper.SquidKeeper().main2() # 当代理重新拨号更换ip后，随后就更新squid.conf文件
        # time.sleep(DIAL_CYCLE)





