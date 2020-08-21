import time
# from requests import ReadTimeout
from requests.exceptions import ConnectionError, ReadTimeout
import requests
from collections import defaultdict
from loguru import logger
TEST_URL = "http://icanhazip.com"
# TEST_URL = "http://www.baidu.com"
TEST_TIMEOUT = 10
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
}

def check(proxy):
    """
    测试代理，返回测试结果
    :param proxy: 代理
    :return: 测试结果
    """
    try:
        response = requests.get(TEST_URL, proxies={
            'http': 'http://' + proxy,
            'https': 'https://' + proxy
            # 'http':  proxy,
            # 'https':  proxy
        }, timeout=TEST_TIMEOUT, headers=headers,verify=False)
        logger.debug(f'Using {proxy} to test {TEST_URL}...')
        if response.status_code == 200:
            print(response.text)
            return True
    except (ConnectionError, ReadTimeout):
        return False

if __name__ == '__main__':
    proxy = "223.243.140.175:3128"
    if check(proxy):
        print("success")