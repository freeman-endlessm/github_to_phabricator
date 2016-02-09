#!/usr/bin/python

import json
from config import *
from github_cache import *

class Member(object):
    def __init__(self, github_dict):
        self.json = github_dict
        self.login = self.json['login']
        self.email = self.json['email']

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


if __name__ == '__main__':
    members = FetchGithubMembers()
    for member in members:
	print "%s:%s" % (member.login, member.email)
