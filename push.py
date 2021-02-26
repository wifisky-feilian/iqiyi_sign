import requests
import json
import os



class push():
    def dingtalk(self,contents):  #钉钉消息推送
        dingding = os.environ["dingding"]
        dd_header = {"Content-Type": "application/json", "Charset": "UTF-8"}
        dd_message = {
            "msgtype": "text",
            "text": {
                "content": f'bilibili每日任务信息通知！\n{contents}'
            }
        }
        r = requests.post(url=dingding,
                        headers=dd_header,
                        data=json.dumps(dd_message))
        if r.status_code == 200:
            print('[+]钉钉消息已推送，请查收\n')
    def start(self,contents):
        self.dingtalk(contents)
