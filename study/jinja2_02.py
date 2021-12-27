# coding: utf-8

from jinja2.environment import Environment
from jinja2 import FileSystemLoader
import ipdb

#ipdb.set_trace()

env = Environment(loader=FileSystemLoader('./'))

#env.filters.update()
#env.tests.update()

template = env.get_template('jinja2_02.j2')

#hosts = {'hosts': [1,2,3,4,5,6]}
#result = template.render(hosts=hosts)

hosts = {'hosts':[1,2,3,4,5,6]}
result = template.render(hosts=hosts)
print result

