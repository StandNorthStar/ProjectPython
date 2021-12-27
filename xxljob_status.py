#!/usr/bin/python3
import bs4.element
import requests
from bs4 import BeautifulSoup
import json
from prettytable import PrettyTable
from colorama import init,Fore
init(autoreset=True)
#通过使用autoreset参数可以让变色效果只对当前输出起作用，输出完成后颜色恢复默认设置


JOBSTATUS= {
    "NORMAL": (Fore.GREEN + "运行" + Fore.RESET),
    "PAUSED": (Fore.RED + "停止" + Fore.RESET),
}

def getExecter()->list:
    url = "http://{url}/xxl-job-admin/jobgroup"
    cookies = {
        "XXL_JOB_LOGIN_IDENTITY": ""
    }
    headers = {
        "Content-Type": "Application/json"
    }

    req = requests.get(url,  headers=headers, cookies=cookies)
    result = str(req.content, encoding="UTF-8")
    soup = BeautifulSoup(result, "html.parser")
    soup.prettify()
    tablelist = soup.find_all('table', id="joblog_list")
    tables = tablelist[0].tbody

    result = []
    for row in tables:
        if isinstance(row, bs4.element.NavigableString):
            continue
        id = row.button.get("id")
        appname = row.button.get("appname")
        title = row.button.get("title")
        result.append({id: (appname,title)})
    return result

def getTasks(jobGroup)->list:
    url = "http://{url}/xxl-job-admin/jobinfo/pageList"
    cookies = {
        "XXL_JOB_LOGIN_IDENTITY": ""
    }
    formData = {
        'jobGroup': jobGroup,
        'jobDesc': "",
        'executorHandler': "",
        'start': 0,
        'length': 1000
    }
    req = requests.post(url, data=formData, cookies=cookies)
    result = str(req.content, encoding="UTF-8")
    data = json.loads(result)

    taskData = data.get("data")
    taskTotal = data.get("recordsTotal")

    result = []
    if taskTotal != 0:
        for job in taskData:
            jobDesc = job.get("jobDesc").strip()
            jobStatus = job.get("jobStatus")
            result.append({jobDesc: jobStatus})
        return result
    else:
        return result


def main():

    table = PrettyTable(["AppName", "AppDesc", "JobDesc", "JobStatus"])
    table.align["AppName"] = "l"
    table.align["AppDesc"] = "l"
    table.align["JobDesc"] = "l"
    for exec in getExecter():
        jobGroup, appinfo = list(exec.items())[0]
        appName, appDesc = appinfo

        tasklist = getTasks(jobGroup)
        if tasklist == []:
            print("NAME:{} NO JOBS".format(appName))
            continue

        job = {}
        for task in tasklist:
            jobDesc, jobStatus = list(task.items())[0]

            job["xxlType"] = "stopController"
            job["appName"] = appName
            job["jobDesc"] = jobDesc
            table.add_row([appName, appDesc, jobDesc, JOBSTATUS[jobStatus]])

    print(table)


if __name__ == "__main__":

    main()