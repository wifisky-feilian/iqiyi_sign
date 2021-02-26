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
    try:
        _push.start(contents)
    except:
        print('[+]推送参数未填写或推送脚本出错')
if __name__ == '__main__':
    main()
