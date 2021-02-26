# -*- coding: utf-8 -*-

import json
import os
import re
import time
import requests

iqiyi_cookie = os.environ["iqiyi_cookie"]
regex = re.compile("P00001=(.*?);")
P00001 = regex.findall(iqiyi_cookie)
p00003 = regex.findall(iqiyi_cookie)


class aiqiyi:
    def __init__(self):
        self.P00001 = P00001
        self.p00003 = p00003
        #任务列表
        self.taskList = []
        # 成长值
        self.growthTask = 0

    #用户信息查询
    def user_information(self):
        time.sleep(3)
        url = "http://serv.vip.iqiyi.com/vipgrowth/query.action"
        #print(self.P00001)
        params = {
            "P00001": self.P00001,
        }
        response = requests.get(url, params=params)
        if response.json()["code"] == "A00000":
            try:
                res_data = response.json()["data"]
                # VIP等级
                level = res_data["level"]
                # 当前VIP成长值
                growthvalue = res_data["growthvalue"]
                # 升级需要成长值
                distance = res_data["distance"]
                # VIP到期时间
                deadline = res_data["deadline"]
                # 今日成长值
                todayGrowthValue = res_data["todayGrowthValue"]
                msg = f"[+]VIP等级：{level}\n[+]当前成长值：{growthvalue}\n[+]升级需成长值：{distance}\n[+]今日成长值:  +{todayGrowthValue}\n[+]VIP到期时间:{deadline}"
            except:
                msg = response.json()
        else:
            # print("（iqy）签到错误", res.content.decode())
            msg = response.json()
        print(msg)
        return msg

    def sign(self):
        '''
        VIP签到
        '''
        url = "https://tc.vip.iqiyi.com/taskCenter/task/queryUserTask"
        params = {"P00001": self.P00001, "autoSign": "yes"}
        response = requests.get(url, params=params)
        if response.json()["code"] == "A00000":
            try:
                growth = response.json(
                )["data"]["signInfo"]["data"]["rewardMap"]["growth"]
                continueSignDaysSum = response.json(
                )["data"]["signInfo"]["data"]["continueSignDaysSum"]
                rewardDay = 7 if continueSignDaysSum % 28 <= 7 else (
                    14 if continueSignDaysSum % 28 <= 14 else 28)
                rouund_day = 28 if continueSignDaysSum % 28 == 0 else continueSignDaysSum % 28
                msg = f"\n[+]签到获得{growth}成长值\n[+]连续签到：{continueSignDaysSum}天\n[+]签到周期：{rouund_day}天/{rewardDay}天"
            except:
                msg = response.json()["data"]["signInfo"]["msg"]
        else:
            msg = response.json()["msg"]
        print(msg)
        return msg

    def queryTask(self):
        '''
        获取VIP日常任务 和 taskCode(任务状态)
        '''
        url = "https://tc.vip.iqiyi.com/taskCenter/task/queryUserTask"
        params = {"P00001": self.P00001}
        response = requests.get(url, params=params)
        if response.json()["code"] == "A00000":
            for item in response.json()["data"]["tasks"]["daily"]:
                #任务列表缓存
                self.taskList.append({
                    "name":
                    item["name"],
                    "taskCode":
                    item["taskCode"],
                    "status":
                    item["status"],
                    "taskReward":
                    item["taskReward"]["task_reward_growth"]
                })
        else:
            pass
        return self

    def joinTask(self):
        """
        遍历完成任务
        """
        url = "https://tc.vip.iqiyi.com/taskCenter/task/joinTask"
        params = {
            "P00001": self.P00001,
        }
        # 遍历任务，仅做一次
        for item in self.taskList:
            if item["status"] == 2:
                #添加参数
                params["taskCode"] = item["taskCode"]
                response = requests.get(url, params=params)
                #print(response.text)
    def getReward(self):
        """
        获取任务奖励
        :return: 返回信息
        """
        url = "https://tc.vip.iqiyi.com/taskCenter/task/getTaskRewards"
        params = {
            "P00001": self.P00001,
        }
        # 遍历任务，领取奖励
        for item in self.taskList:
            if item["status"] == 0:
                params["taskCode"] = item["taskCode"]
                response = requests.get(url, params=params)
                #print(response.text)
                if response.json()["code"] == "A00000":
                    self.growthTask += item["taskReward"]
        msg = f"\n[+]完成任务获得{self.growthTask}成长值"
        print(msg)
        return msg

    def start(self):
        #签到
        sign_msg = self.sign()
        #获取任务列表
        self.queryTask()
        #遍历做任务
        self.joinTask()
        #获取任务奖励
        growth_value = self.getReward()
        #查询用户信息
        user_msg = self.user_information()
        msg = user_msg + sign_msg + growth_value
        #print(msg)
        return msg