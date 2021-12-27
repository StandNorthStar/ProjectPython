#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import argparse
import json
import yaml
import os
from jinja2.environment import Environment
from jinja2 import FileSystemLoader
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.web import Application, RequestHandler
from tornado.httpclient import HTTPRequest

import sys
reload(sys)
sys.setdefaultencoding('utf8')


class AlertInfo(RequestHandler):

    def post(self):
        self.enterprise = json.loads(self.request.body)
        self.get_template()
        self.reload_service()

    def get_template(self):
        env = Environment(loader=FileSystemLoader('./'))
        template = env.get_template('alert1.yml.j2')
        result = template.render(alert_info=self.enterprise)

        template_dir = os.path.dirname(os.path.abspath(__file__))
        template_dir_base = os.path.join(template_dir, 'enterprise')

        file_name = 'rules_' + self.enterprise.keys()[0] + '.yml'
        file_path = os.path.join(template_dir_base, file_name)

        #print result
        with open(file_path, 'w') as f:
            f.write(result)
        print "write ok"        
   
    def reload_service(self):
        headers = {
            "Content-Type": "application/json"
        }
        #request = HTTPRequest('http://192.168.10.107:9090/-/reload', method='POST', headers=headers)
        re = requests.post('http://192.168.10.107:9090/-/reload', headers=headers)
        print re.status_code

if __name__ == "__main__":
     app = Application(
         [(r"/config/$", AlertInfo),],
     )
     server = HTTPServer(app)
     server.listen(80)
     #server.bind(args.web_port)
     #server.start()
     IOLoop.current().start()


