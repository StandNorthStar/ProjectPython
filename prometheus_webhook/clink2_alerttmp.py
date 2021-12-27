# coding: utf-8

from jinja2.environment import Environment
from jinja2 import FileSystemLoader
from jinja2 import Template
import ipdb
import yaml

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')  
env = Environment(loader=FileSystemLoader('./'))
template = env.get_template('alert1.yml.j2')
template_file = '/data/python-project/prometheus_webhook/alert1.yml.j2'

enterprise = {'1010':[
	{"name": "cpu_alert", "value": 80, "status": True}, 
	{"name": "memory_alert", "value": 1000000000, "status": True}
   ]
}

result = template.render(alert_info=enterprise)
print result
#x = yaml.load(result)
#print x
