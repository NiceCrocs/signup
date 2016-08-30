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
import webapp2
import re
import cgi

form = """
<!DOCTYPE html>

<html>
    <head>
        <style>
            .error {
                color: red;
            }
        </style>
    </head>
    <body>
    <h1>Signup</h1>
        <form method="post">
            <table>
                <tr>
                    <td><label for="username">Username</label></td>
                    <td>
                        <input name="username" type="text" value="%(e)s" required>
                        <span class="error">%(a)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="password">Password</label></td>
                    <td>
                        <input name="password" type="password" required>
                        <span class="error">%(b)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="verify">Verify Password</label></td>
                    <td>
                        <input name="verify" type="password" required>
                        <span class="error">%(c)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="email">Email (optional)</label></td>
                    <td>
                        <input name="email" type="email" value="%(f)s">
                        <span class="error">%(d)s</span>
                    </td>
                </tr>
            </table>
            <input type="submit">
        </form>
    </body>
</html>"""

welcome_form = """
<head>
    <title>Congratulations!</title>
</head>
<body>
    <h1>Welcome, %(e)s!</h1>
</body>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Signup(webapp2.RequestHandler):

    def get(self):
        self.response.write(form % {"a": "", "b": "", "c": "", "d": "", "e": "", "f": ""})

    def post(self):
        have_error1 = False
        have_error2 = False
        have_error3 = False
        have_error4 = False
        error_username = ""
        error_password = ""
        error_verify = ""
        error_email = ""
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        if not valid_username(username):
            error_username = "That's not a valid username."
            have_error1 = True

        if not valid_password(password):
            error_password = "That wasn't a valid password."
            have_error2 = True
        elif password != verify:
            error_verify = "Your passwords didn't match."
            have_error3 = True

        if not valid_email(email):
            error_email = "That's not a valid email."
            have_error4 = True

        if have_error1 or have_error2 or have_error3 or have_error4:
            username = cgi.escape(username, quote = True)
            email = cgi.escape(email, quote = True)
            self.response.write(
                form % {
                "a": error_username,
                "b": error_password,
                "c": error_verify,
                "d": error_email,
                "e": username,
                "f": email})

        else:
            self.redirect('/Welcome?username={}'.format(username))

class WelcomePage(webapp2.RequestHandler):

    def get(self):
        username = self.request.get('username')
        self.response.write(welcome_form % {'e': username})

app = webapp2.WSGIApplication([('/', Signup),
                               ('/Welcome', WelcomePage)],
                              debug=True)
