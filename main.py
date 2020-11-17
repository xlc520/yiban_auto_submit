import json
import random
import time
import traceback
from yiban import YiBan
import util
if __name__ == '__main__':
    try:
        yb = YiBan("phone", "password") # FIXME:账号密码
        yb.login()
        yb.getHome()
        print("登录成功 %s"%yb.name)
        yb.auth()
        all_task = yb.getUncompletedList()["data"]
        all_task = list(filter(lambda x: "体温检测" in x["Title"], all_task))  # FIXME: 长理的打卡任务标题均含有"体温检测"字样 此举是防止其他表单干扰 （可能会变）
        if len(all_task) == 0:
            print("没找到今天长理体温上报的任务，可能是你已经上报，如果不是请手动上报。")
        else:
            all_task_sort = util.desc_sort(all_task, "StartTime")  # 按开始时间排序
            new_task = all_task_sort[0]  # 只取一个最新的
            print("找到未上报的任务：", new_task)
            task_detail = yb.getTaskDetail(new_task["TaskId"])["data"]
            ex = {"TaskId": task_detail["Id"],
                "title": "任务信息",
                "content": [{"label": "任务名称", "value": task_detail["Title"]},
                            {"label": "发布机构", "value": task_detail["PubOrgName"]},
                            {"label": "发布人", "value": task_detail["PubPersonName"]}]}
            # FIXME: 以下是长沙理工大学最新的表单信息，由于某些值（检测时间）必须是动态的，所以只能将form表单写死在这里 （可能会变）
            dict_form = {"2fca911d0600717cc5c2f57fc3702787": ["湖南省", "长沙市", "天心区"],
                        "cab886bf693f23a34ed78ed71deaadc3": yb.name,
                        "b418fa886b6a38bdce72569a70b1fa10": ["36.2", "36.3", "36.4", "36.5", "36.6", "36.7", "36.8"][random.randint(0, 6)], # 随机体温
                        "c77d35b16fb22ec70a1f33c315141dbb": util.get_time_no_second()}
            submit_result = yb.submit(json.dumps(dict_form, ensure_ascii=False), json.dumps(
                ex, ensure_ascii=False), task_detail["WFId"])
            if submit_result["code"] == 0:
                share_url = yb.getShareUrl(submit_result["data"])["data"]["uri"]
                print("已完成一次体温上报[%s]" % task_detail["Title"])
                print("访问此网址查看详情：%s" % share_url)
            else:
                print("[%s]遇到了一些错误:%s" % (task_detail["Title"], submit_result["msg"]))
    except Exception as e:
        print("出错啦")
        print(e)
