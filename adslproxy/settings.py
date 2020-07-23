# coding=utf-8
from environs import Env

env = Env()

# 拨号间隔，单位秒
DIAL_CYCLE = env.int('DIAL_CYCLE', 120)

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
SERVER_PORT = env.int('SERVER_PORT', 23791)
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
SQUID_KEEPER_INTERVAL = 60


# adsl 拨号服务器集群
ADSL_SERVERS = [
# 江西萍乡电信拨号VPS1型
    {"CLIENT_NAME": 'vpseqjfvw', "ADSLHOST": "218.87.123.58", "ADSLPORT": "20275", "ADSLUSER": "root",
     "ADSLPWD": "w8RwjFrnB2FQs"},
    # 江西萍乡电信拨号VPS2型
    {"CLIENT_NAME": 'adsl01', "ADSLHOST": "218.87.123.58", "ADSLPORT": "20175", "ADSLUSER": "root",
     "ADSLPWD": "g9asioc7FbGGg"},
    {"CLIENT_NAME": 'adsl02', "ADSLHOST": "218.87.123.58", "ADSLPORT": "20401", "ADSLUSER": "root",
     "ADSLPWD": "g9asioc7FbGGg"},
    {"CLIENT_NAME": 'adsl03', "ADSLHOST": "218.87.123.58", "ADSLPORT": "20413", "ADSLUSER": "root",
     "ADSLPWD": "Lnn2u8x883Syn"},
    {"CLIENT_NAME": 'adsl04', "ADSLHOST": "218.87.123.58", "ADSLPORT": "20415", "ADSLUSER": "root",
     "ADSLPWD": "Lnn2u8x883Syn"},
    {"CLIENT_NAME": 'adsl05', "ADSLHOST": "218.87.123.58", "ADSLPORT": "20423", "ADSLUSER": "root",
     "ADSLPWD": "Lnn2u8x883Syn"},
    {"CLIENT_NAME": 'adsl06', "ADSLHOST": "218.87.123.58", "ADSLPORT": "20439", "ADSLUSER": "root",
     "ADSLPWD": "Lnn2u8x883Syn"},
    {"CLIENT_NAME": 'adsl07', "ADSLHOST": "218.87.123.58", "ADSLPORT": "20443", "ADSLUSER": "root",
     "ADSLPWD": "Lnn2u8x883Syn"},
    {"CLIENT_NAME": 'adsl08', "ADSLHOST": "218.87.123.58", "ADSLPORT": "20459", "ADSLUSER": "root",
     "ADSLPWD": "Lnn2u8x883Syn"},
    {"CLIENT_NAME": 'adsl09', "ADSLHOST": "218.87.123.58", "ADSLPORT": "20331", "ADSLUSER": "root",
     "ADSLPWD": "Lnn2u8x883Syn"},
    {"CLIENT_NAME": 'adsl010', "ADSLHOST": "218.87.123.58", "ADSLPORT": "20449", "ADSLUSER": "root",
     "ADSLPWD": "Lnn2u8x883Syn"},
    {"CLIENT_NAME": 'adsl011', "ADSLHOST": "218.87.123.58", "ADSLPORT": "20297", "ADSLUSER": "root",
     "ADSLPWD": "Lnn2u8x883Syn"},
    {"CLIENT_NAME": 'adsl012', "ADSLHOST": "218.87.123.58", "ADSLPORT": "20299", "ADSLUSER": "root",
     "ADSLPWD": "Lnn2u8x883Syn"},
    #湖南常德电信拨号VPS2型
    {"CLIENT_NAME": 'adslh02', "ADSLHOST": "223.151.49.32", "ADSLPORT": "20091", "ADSLUSER": "root",
     "ADSLPWD": "3mTz9F1eQoOeI"},
    {"CLIENT_NAME": 'adslh01', "ADSLHOST": "223.151.49.32", "ADSLPORT": "20083", "ADSLUSER": "root",
     "ADSLPWD": "3mTz9F1eQoOeI"},
    {"CLIENT_NAME": 'adslh03', "ADSLHOST": "223.151.49.32", "ADSLPORT": "20097", "ADSLUSER": "root",
     "ADSLPWD": "3mTz9F1eQoOeI"},
    {"CLIENT_NAME": 'adslh04', "ADSLHOST": "223.151.49.32", "ADSLPORT": "20103", "ADSLUSER": "root",
     "ADSLPWD": "3mTz9F1eQoOeI"},
    {"CLIENT_NAME": 'adslh05', "ADSLHOST": "223.151.49.32", "ADSLPORT": "20107", "ADSLUSER": "root",
     "ADSLPWD": "3mTz9F1eQoOeI"},
    {"CLIENT_NAME": 'adslh06', "ADSLHOST": "223.151.49.32", "ADSLPORT": "20111", "ADSLUSER": "root",
     "ADSLPWD": "3mTz9F1eQoOeI"},
    {"CLIENT_NAME": 'adslh07', "ADSLHOST": "223.151.49.32", "ADSLPORT": "20115", "ADSLUSER": "root",
     "ADSLPWD": "3mTz9F1eQoOeI"},
    {"CLIENT_NAME": 'adslh08', "ADSLHOST": "223.151.49.32", "ADSLPORT": "20119", "ADSLUSER": "root",
     "ADSLPWD": "3mTz9F1eQoOeI"},
    {"CLIENT_NAME": 'adslh09', "ADSLHOST": "223.151.49.32", "ADSLPORT": "20121", "ADSLUSER": "root",
     "ADSLPWD": "3mTz9F1eQoOeI"},
    {"CLIENT_NAME": 'adslh010', "ADSLHOST": "223.151.49.32", "ADSLPORT": "20125", "ADSLUSER": "root",
     "ADSLPWD": "3mTz9F1eQoOeI"},
    {"CLIENT_NAME": 'adslh011', "ADSLHOST": "223.151.49.32", "ADSLPORT": "20141", "ADSLUSER": "root",
     "ADSLPWD": "3mTz9F1eQoOeI"},
    {"CLIENT_NAME": 'adslh012', "ADSLHOST": "223.151.49.32", "ADSLPORT": "20149", "ADSLUSER": "root",
     "ADSLPWD": "3mTz9F1eQoOeI"},
    {"CLIENT_NAME": 'adslh013', "ADSLHOST": "223.151.49.32", "ADSLPORT": "20203", "ADSLUSER": "root",
     "ADSLPWD": "3mTz9F1eQoOeI"},
    # 浙江宁波电信拨号VPS2型
    {"CLIENT_NAME": 'adsls01', "ADSLHOST": "122.227.184.60", "ADSLPORT": "20143", "ADSLUSER": "root",
     "ADSLPWD": "BV27CitP6sxqC"},
    {"CLIENT_NAME": 'adsls02', "ADSLHOST": "122.227.184.60", "ADSLPORT": "20151", "ADSLUSER": "root",
     "ADSLPWD": "BV27CitP6sxqC"},
    {"CLIENT_NAME": 'adsls03', "ADSLHOST": "122.227.184.60", "ADSLPORT": "20159", "ADSLUSER": "root",
     "ADSLPWD": "BV27CitP6sxqC"},
    {"CLIENT_NAME": 'adsls04', "ADSLHOST": "122.227.184.60", "ADSLPORT": "20161", "ADSLUSER": "root",
     "ADSLPWD": "BV27CitP6sxqC"},
    {"CLIENT_NAME": 'adsls05', "ADSLHOST": "122.227.184.60", "ADSLPORT": "20163", "ADSLUSER": "root",
     "ADSLPWD": "BV27CitP6sxqC"},
    {"CLIENT_NAME": 'adsls06', "ADSLHOST": "122.227.184.60", "ADSLPORT": "20183", "ADSLUSER": "root",
     "ADSLPWD": "BV27CitP6sxqC"},
    {"CLIENT_NAME": 'adsls07', "ADSLHOST": "122.227.184.60", "ADSLPORT": "20189", "ADSLUSER": "root",
     "ADSLPWD": "BV27CitP6sxqC"},
    {"CLIENT_NAME": 'adsls08', "ADSLHOST": "122.227.184.60", "ADSLPORT": "20203", "ADSLUSER": "root",
     "ADSLPWD": "BV27CitP6sxqC"},
    {"CLIENT_NAME": 'adsls09', "ADSLHOST": "122.227.184.60", "ADSLPORT": "20211", "ADSLUSER": "root",
     "ADSLPWD": "BV27CitP6sxqC"},
    {"CLIENT_NAME": 'adsls010', "ADSLHOST": "122.227.184.60", "ADSLPORT": "20213", "ADSLUSER": "root",
     "ADSLPWD": "BV27CitP6sxqC"},
    {"CLIENT_NAME": 'adsls011', "ADSLHOST": "122.227.184.60", "ADSLPORT": "20217", "ADSLUSER": "root",
         "ADSLPWD": "BV27CitP6sxqC"},
    {"CLIENT_NAME": 'adsls012', "ADSLHOST": "122.227.184.60", "ADSLPORT": "20257", "ADSLUSER": "root",
         "ADSLPWD": "BV27CitP6sxqC"},
    {"CLIENT_NAME": 'adsls013', "ADSLHOST": "122.227.184.60", "ADSLPORT": "20259", "ADSLUSER": "root",
     "ADSLPWD": "BV27CitP6sxqC"},
    ##内蒙古包头电信拨号VPS2型
    {"CLIENT_NAME": 'adslb2', "ADSLHOST": "1.180.56.166", "ADSLPORT": "20157", "ADSLUSER": "root",
     "ADSLPWD": "4QNkRbKhMlP4b"},
    {"CLIENT_NAME": 'adslb1', "ADSLHOST": "1.180.56.166", "ADSLPORT": "20153", "ADSLUSER": "root",
     "ADSLPWD": "4QNkRbKhMlP4b"},


]