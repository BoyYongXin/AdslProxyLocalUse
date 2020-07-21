# -*-coding=utf-8 -*-
from multiprocessing.dummy import Pool as ThreadPool
import re
import requests
import requests
import paramiko
from requests.exceptions import ConnectionError, ReadTimeout
from loguru import logger
import time
from retrying import retry, RetryError
import redis
from adslproxy.db import RedisClient
from adslproxy.settings import *

# TEST_URL = "https://blog.csdn.net/weixin_34174105/article/details/89794550"
TEST_URL = "http://www.httpbin.org/ip"
def test_proxy( proxy):
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
            print(response.text)
            return True
    except (ConnectionError, ReadTimeout):
        return False
if __name__ == '__main__':
    proxy = "10.103.17.235:3201"
    # proxy = "121.56.38.69:3128"
    for i in range(10):
        if test_proxy(proxy):
            print('sussess')