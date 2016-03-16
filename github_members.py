#!/usr/bin/python

import json
import random
import string
from config import *
from github_cache import *
from wmfphablib.phabapi import phabapi

from lib_user_map import *

class Member(object):
    def __init__(self, github_dict):
        self.json = github_dict
        self.login = self.json['login']
        if self.json['name']:
            self.name = self.json['name']
        else:
            self.name = ""
        if self.json['name']:
            self.email = self.json['email']
        else:
            self.email = ""

def FetchGithubMembers():
    page = 1
    num_pages = 1

    members = []
    github_members = []

    while page <= num_pages:
        (headers, members_json) = fetch_json("/orgs/%s/members?per_page=100&page=%d" % (USER,page))
        page = page + 1
        members.extend(json.loads(members_json))
        headers = headers.split('\r\n')
        for header in headers[1:]:
            (key, value) = header.split(":", 1)
            if key == "Link":
                try:
                    value.index('rel="next"')
                    num_pages = page
                except:
                    pass
                break

    for i in members:
        (headers, member_json) = fetch_json("/users/%s" % (i["login"]))
        member = Member(json.loads(member_json))
        github_members.append(member)

    return sorted(github_members)

def gen_password():
    chars = string.letters + string.digits
    newpasswd = ""
    for i in range(8):
        newpasswd = newpasswd + random.choice(chars)
    return newpasswd

if __name__ == '__main__':
    from wmfphablib import phabapi
    from phabricator import APIError
    api = phabapi.phabapi()
    members = FetchGithubMembers()
    for member in members:
        print "#%s" % (member.login)
        login = member.login.lower()
        user = tr_user(member.login)
        name = tr_user_name(member.login)
        if CREATE_ACCOUNTS != True:
            continue
        password=gen_password()
        if user != None:
            email = "%s@%s"%(user,ACCOUNT_EMAIL_DOMAIN)
        else:
            email = "no-reply-github-user-%s@%s"%(login,ACCOUNT_EMAIL_DOMAIN)
        if name == None:
            name = login
        try:
            api.create_user(login, name, email, password)
        except APIError, e:
            print "Warning: Failed to create user %s: %s"%(login, e)
        else:
            print "%s,%s"%(login, password)
