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
            return True
    except (ConnectionError, ReadTimeout):
        return False
if __name__ == '__main__':
    proxy = "182.99.251.232:3128"
    if test_proxy(proxy):
        print('sussess')