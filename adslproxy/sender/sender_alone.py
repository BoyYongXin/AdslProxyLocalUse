import re
import requests
import paramiko
from requests.exceptions import ConnectionError, ReadTimeout
from loguru import logger
import time
from retrying import retry, RetryError
import redis
from adslproxy.db import RedisClient
from environs import Env
env = Env()

# 客户端唯一标识
CLIENT_NAME = env.str('CLIENT_NAME', 'vpseqjfvw')
ADSLHOST = ""
ADSLPORT = ""
ADSLUSER = ""
ADSLPWD = ""


TEST_URL = "https://www.baidu.com"
TEST_TIMEOUT = 10
DIAL_CYCLE = 100

# Redis数据库IP
REDIS_HOST = env.str('REDIS_HOST', '10.126.30.6')
# Redis数据库密码, 如无则填None
REDIS_PASSWORD = env.str('REDIS_PASSWORD', None)
# Redis数据库端口
REDIS_PORT = env.int('REDIS_PORT', 6379)
# 代理池键名
REDIS_KEY = env.str('REDIS_KEY', 'adsl1')

# 代理端口
PROXY_PORT = env.int('PROXY_PORT', 3128)

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

    def test_proxy(self, proxy):
        """
        测试代理，返回测试结果
        :param proxy: 代理
        :return: 测试结果
        """
        try:
            response = requests.get(TEST_URL, proxies={
                'http': 'http://' + proxy,
                'https': 'https://' + proxy
            }, timeout=TEST_TIMEOUT)
            if response.status_code == 200:
                return True
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
        logger.info(f'Removing {CLIENT_NAME}...')
        try:
            # 由于拨号就会中断连接，所以每次都要重新建立连接
            if hasattr(self, 'redis') and self.redis:
                self.redis.close()
            self.redis = RedisClient()
            self.redis.remove(CLIENT_NAME)
            logger.info(f'Removed {CLIENT_NAME} successfully')
            return True
        except redis.ConnectionError:
            logger.info(f'Remove {CLIENT_NAME} failed')

    def set_proxy(self, proxy):
        """
        设置代理
        :param proxy: 代理
        :return: None
        """
        self.redis = RedisClient()
        if self.redis.set(CLIENT_NAME, proxy):
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
        m = Monitor(ADSLHOST, ADSLPORT, ADSLUSER, ADSLPWD)
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
                time.sleep(DIAL_CYCLE)
            else:
                logger.error(f'Proxy invalid {proxy}')
        else:
            # 获取 IP 失败，重新拨号
            logger.error('Get IP failed, re-dialing')
            self.run()


def send(loop=True):
    sender = Sender()
    sender.loop() if loop else sender.run()


if __name__ == '__main__':
    send()