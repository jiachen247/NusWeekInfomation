#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import json
from google.appengine.ext import ndb

import webapp2

from WeekInfomation import WeekInfomation

KEY_NAME = "SCHOOL_CALENDAR"


class Week(ndb.Model):
    info = ndb.StringProperty()
    lastUpdated = ndb.DateTimeProperty(auto_now_add=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        info = Week.get_by_id(KEY_NAME)

        if info is None:
            info = Week(info="-")

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(info.info)


class WeeklyHandler(webapp2.RequestHandler):
    def get(self):
        info = Week.get_by_id(KEY_NAME)

        if info is None:
            info = Week(id=KEY_NAME)

        info.info = WeekInfomation().get()

        info.put()
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write("info: " + info.info)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/weekly', WeeklyHandler),
], debug=True)
