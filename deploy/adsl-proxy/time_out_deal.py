# coding=utf-8
'''
超时装饰器作用：
    场景： 运行某个函数时，由于各种原因，导致函数执行时间，拉长，导致后面的模块，无法正常使用，
    或者延迟使用

    解决思路：
        设置函数执行时间，超时则执行，下一个备用的解决函数，避免，后面的功能模块，正常使用
'''
import signal
import time

def set_timeout(num, callback):
    def wrap(func):
        def handle(signum, frame):  # 收到信号 SIGALRM 后的回调函数，第一个参数是信号的数字，第二个参数是the interrupted stack frame.
            raise RuntimeError

        def to_do(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handle)  # 设置信号和回调函数
                signal.alarm(num)  # 设置 num 秒的闹钟
                print('start alarm signal.')
                r = func(*args, **kwargs)
                print('close alarm signal.')
                signal.alarm(0)  # 关闭闹钟
                return r
            except RuntimeError as e:
                callback()

        return to_do

    return wrap


def after_timeout():  # 超时后的处理函数
    print("Time out!")
    raise Exception


@set_timeout(2, after_timeout)  # 限时 2 秒超时
def connect():  # 要执行的函数
    time.sleep(3)  # 函数执行时间，写大于2的值，可测试超时
    print('Finished without timeout.')


if __name__ == '__main__':

    while True:
        try:
            connect()
        except:
            print("执行aaaaa")
            time.sleep(10)
            continue

