# -*- coding: utf-8 -*-
from loguru import logger
import settings
import time
import os
import subprocess
from db import RedisClient

class SquidKeeper:

    def __init__(self):
        self.server = RedisClient()
        # 区别对待使用密码和不使用密码的配置模板
        if settings.USE_PASSWORD:
            self.peer_conf = "cache_peer %s parent %s 0 weighted-round-robin weight=2\n"
            # self.peer_conf = "cache_peer %s parent %s 0 no-query proxy-only login={}:{} never_direct allow all round-robin weight=1 connect-fail-limit=2 allow-miss max-conn=5\n".format(
            #     settings.USERNAME, settings.PASSWORD)
        else:
            self.peer_conf = "cache_peer %s parent %s 0 weighted-round-robin weight=2\n"
            # self.peer_conf = "cache_peer %s parent %s 0 no-query weighted-round-robin weight=2 connect-fail-limit=2 allow-miss max-conn=5\n"

    def read_new_ip(self):
        """
        从redis中读取全部有效ip
        :return:
        """
        logger.info('读取代理池中可用ip')
        proxy_ips = self.server.all()
        return proxy_ips

    def update_conf(self, proxy_list):
        """
        根据读取到的代理ip，和现有配置文件模板，
        生成新的squid配置文件并重新加载，让squid使用最新的ip。
        :param proxy_list:
        :return:
        """
        logger.info('准备加载到squid中')
        with open('squid.conf', 'r') as f:
            squid_conf = f.readlines()
        squid_conf.append('\n# Cache peer config\n')
        squid_conf.append('\nhttp_port 3201 vhost\n')
        for proxy in proxy_list:
            ip, port = proxy.decode('utf8').split(':')
            squid_conf.append(self.peer_conf % (ip, port))
        with open('/etc/squid/squid.conf', 'w') as f:
            f.writelines(squid_conf)
        # failed = os.system('squid -k reconfigure') #重新读写配置文件
        if os.system('squid -k shutdown') > 0:
            os.system('squid -k shutdown')
        failed = os.system('squid -f /etc/squid/squid.conf') #重新读写配置文件
        # 这是一个容错措施
        # 当重新加载配置文件失败时，会杀死全部相关进行并重试
        if failed > 0:
            logger.info('squid进程出现问题，查找当前启动的squid相关进程...')
            p = subprocess.Popen("ps -ef | grep squid | grep -v grep  | awk '{print $2}'", shell=True,
                                 stdout=subprocess.PIPE, universal_newlines=True)
            p.wait()
            result_lines = [int(x.strip()) for x in p.stdout.readlines()]
            logger.info('找到如下进程：{}'.format(result_lines))
            if len(result_lines):
                for proc_id in result_lines:
                    logger.info('开始杀死进程 {}...'.format(proc_id))
                    os.system('kill -s 9 {}'.format(proc_id))
            logger.info('全部squid已被杀死，开启新squid进程...')
            os.system('service squid restart')
            time.sleep(3)
            logger.info('重新加载ip...')
            # os.system('squid -k reconfigure')
            os.system('squid -f /etc/squid/squid.conf')
        logger.info('当前可用IP数量 {}'.format(len(proxy_list)))

    def main(self):
        """
        周期性地更新squid的配置文件，
        使其使用最新的代理ip
        :return:
        """
        while True:
            proxy_lists = []
            proxy_list = self.read_new_ip()
            for proxy in proxy_list.values():
                proxy_lists.append(proxy)
            print(proxy_lists)
            break
            # self.update_conf(proxy_lists)
            # logger.info('*' * 40)
            # time.sleep(settings.SQUID_KEEPER_INTERVAL)


if __name__ == '__main__':
    SquidKeeper().main()
