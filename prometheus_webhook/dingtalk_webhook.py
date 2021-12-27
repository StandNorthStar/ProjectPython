#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import argparse
import json
import jinja2
import os

from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.web import Application, RequestHandler


parse = argparse.ArgumentParser()
parse.add_argument("--web-port", default=8686, help="Server Listen Port(Default 8686)")
parse.add_argument("--webhook", help="dingding webhook URL")
args = parse.parse_args()

class AlertInfo(RequestHandler):
 
    def post(self):
        self.result = json.loads(self.request.body)
        self.sendinfo(self.result)
        
    def sendinfo(self, messages):
        template_dir = os.path.dirname(os.path.abspath(__file__))
        template_file = 'sendinfo.md.j2'
        print template_dir
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir, encoding='utf-8'))
        template = env.get_template(template_file)
            
        messages = template.render(messages)
        if args.webhook:       
            url = args.webhook
            headers = {
                "Content-Type": "Application/json"
            }
            data = dict(
                #msgtype = "text",
                #text=dict(
                #    content = mark
                #),
                #at=dict(
                #    atMobiles = [""]
                #)
                msgtype="markdown",
                markdown=dict(
                    title="test",
                    text=messages
                ),
            )
            req = requests.post(url, data=json.dumps(data), headers=headers) 
            result = req.content
            print result
            return result
        else:
            print "Please settting --webhook arg"

if __name__ == "__main__":
        
     app = Application([
         (r"/alertinfo/$", AlertInfo),
     ])
     server = HTTPServer(app)
     server.listen(args.web_port)
     #server.bind(args.web_port)
     #server.start()
     IOLoop.current().start()


