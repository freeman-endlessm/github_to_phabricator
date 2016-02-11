#!/usr/bin/python

import csv
user_map = {}
with open('user_map.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        github_login=row[0].strip()
        google_account=row[1].strip()
        real_name=row[2].strip()
        if len(row) >= 3 and github_login != "" and google_account != "":
            user_map[github_login]={
                'account': google_account,
                'name': real_name,
            }

def tr_user(user):
    if user_map.has_key(user) and user_map[user]['account'] != "":
        return user_map[user]['account']
    else:
        return None

def tr_user_name(user):
    if user_map.has_key(user):
        return user_map[user]['name']
    else:
        return None

