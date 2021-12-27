#!/usr/bin/python3
import bs4.element
import requests
from bs4 import BeautifulSoup
import json
import yaml
from prettytable import PrettyTable

# import ipdb
# ipdb.set_trace()

def getExecter()->list:
    url = "http:///xxl-job-admin/jobgroup"
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

    # pttable = PrettyTable(["ID","IPLIST", "APPName", "Title"])
    # pttable.align["IPLIST"] = "l"
    # pttable.align["APPName"] = "l"
    # pttable.align["Title"] = "l"

    result = []
    for row in tables:
        if isinstance(row, bs4.element.NavigableString):
            continue
        id = row.button.get("id")
        addresslist = row.button.get("addresslist")
        appname = row.button.get("appname")
        title = row.button.get("title")
        #pttable.add_row([id, addresslist, appname, title])
        result.append({id: appname})
    #print(pttable)
    return result

def getTasks(jobGroup)->list:
    url = "http://url/xxl-job-admin/jobinfo/pageList"
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


def main(yamlfile):
    yaml.Dumper.ignore_aliases = lambda *args: True
    with open(yamlfile, 'r+', ) as f:
        xxl_job = {
            "xxljob": {
                "version": "1.0.0",
                "data": []
            }
        }
        xxldata = []

        table = PrettyTable(["AppName", "JobDesc", "JobStatus"])
        table.align["AppName"] = "l"
        table.align["JobDesc"] = "l"
        for exec in getExecter():
            jobGroup, appName = list(exec.items())[0]
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
                table.add_row([appName, jobDesc, jobStatus])
            xxldata.append(job)
        print(table)

        xxl_job["xxljob"]["data"] = xxldata
        yaml.dump(xxl_job, f, encoding="utf-8",default_flow_style=False,allow_unicode=True)


if __name__ == "__main__":
    # yamlfile = "/opt/xxl/v1_xxl.yaml"
    yamlfile = "./v1_xxl.yaml"
    main(yamlfile)
