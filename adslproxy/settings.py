# coding=utf-8
from environs import Env

env = Env()

# 拨号间隔，单位秒
DIAL_CYCLE = env.int('DIAL_CYCLE', 100)

# Redis数据库IP
REDIS_HOST = env.str('REDIS_HOST', '10.126.30.6')
# Redis数据库密码, 如无则填None
REDIS_PASSWORD = env.str('REDIS_PASSWORD', None)
# Redis数据库端口
REDIS_PORT = env.int('REDIS_PORT', 6379)
# 代理池键名
REDIS_KEY = env.str('REDIS_KEY', 'adsl1')

# 测试URL
TEST_URL = env.str('TEST_URL', 'http://www.baidu.com')
# 测试最大失败次数
TEST_MAX_ERROR_COUNT = env.int('TEST_MAX_ERROR_COUNT', 10)
# 测试超时时间
TEST_TIMEOUT = env.int('TEST_TIMEOUT', 20)
# 测试周期
TEST_CYCLE = env.int('TEST_CYCLE', 100)

# 服务器端口
SERVER_PORT = env.int('SERVER_PORT', 20275)
SERVER_HOST = env.str('SERVER_HOST', '0.0.0.0')

# 代理端口
PROXY_PORT = env.int('PROXY_PORT', 3128)
PROXY_USERNAME = env.str('PROXY_USERNAME', '')
PROXY_PASSWORD = env.str('PROXY_PASSWORD', '')


#----------squid-keeper-----------
# 代理是否需要通过密码访问,当此项为False时可无视USERNAME和PASSWORD的配置
USE_PASSWORD = False
# 无密码限制时可无视此项，并将USE_PASSWORD改为False
USERNAME = 'your_username'
# 密码
PASSWORD = 'your_password'
# squid从redis中加载新ip的频率
SQUID_KEEPER_INTERVAL = 30


# adsl 拨号服务器集群
ADSL_SERVERS = [

]