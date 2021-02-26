from iqiyi import aiqiyi
from push import push

'''脚本入口'''
def main():
    #创建任务对象
    _aiqiyi=aiqiyi()
    contents=_aiqiyi.start()
    #创建信息推送对象
    _push = push()
    #钉钉推送
    _push.start(contents)
if __name__ == '__main__':
    main()