#!/usr/bin/python

import re
import string
import sys
import urllib2
from github_issues import FetchGithubIssues
from wmfphablib import phabdb
from wmfphablib import phabapi
from wmfphablib import util
from wmfphablib import config

from config import *

github_issues = FetchGithubIssues()
api = phabapi.phabapi()
project_phid = api.get_project_phid(config.project_name)
re_attachment=re.compile("\!?\[(.*?)\]\((.*?githubusercontent.*?)\)")

def lower_snake_caseify(s):
    return "_".join(re.sub(r'\W+', ' ', s.lower()).split(None))

if project_phid is None:
    print "Could not find the project '%s' in Phabricator" % config.project_name
    sys.exit(-1)

if config.have_db_access is False and (config.delete_existing_issues or config.force_ids):
    print "You cannot delete existing taks or force task IDs if you do not have DB access"
    sys.exit(-1)

if config.delete_existing_issues:
    tasks = phabdb.get_task_list()
    for task in tasks:
        projects = phabdb.get_task_projects(task)
        if project_phid in projects:
            print "Deleting %s" % task
            util.destroy_issue(task)

if config.force_ids and len(phabdb.get_task_list()) > 0:
    print "You should not force task ID if there are still existing tasks in maniphest"
    sys.exit(-1)

for issue in github_issues:
    print "Migrating issue %d" % issue.id
    author_phid = api.get_phid_by_username(issue.author)
    assignee_phid = None if issue.assignee is None else api.get_phid_by_username(issue.assignee)
    if issue.description == None:
        clean_issue_description = ""
    else:
        clean_issue_description = issue.description
    for re_obj in CLEAN_DESCRIPTION_REGEXES:
        clean_issue_description = re_obj.sub("",clean_issue_description)
    description = "= Task migrated from github issue #%d which was available at %s =\n\n%s" % (issue.id, issue.url, clean_issue_description)
    if config.have_db_access is False or author_phid is None:
        description = "> Issue originally made by **%s** on //%s//\n\n%s" % (issue.author, issue.created_at, description)
    new_task = api.task_create(issue.title, description, issue.id, 90, assignee_phid, [project_phid])
    phid = new_task['phid']
    print " => Phabricator Task: " + phid
    if config.force_ids:
        phabdb.set_task_id(issue.id, phid)
        id = issue.id
    else:
        id = new_task['id']

    if config.have_db_access:
        if author_phid:
            phabdb.set_task_author(author_phid, id)
        phabdb.set_task_ctime(phid, issue.created_at.strftime("%s"))
        phabdb.set_task_mtime(phid, issue.updated_at.strftime("%s"))

    if issue.state != "open":
        api.set_status(id, "resolved")
        if config.have_db_access:
            if issue.closed_at:
                tphid = phabdb.last_state_change(phid)
                phabdb.set_transaction_time(tphid, issue.closed_at.strftime("%s"))

    if config.static_custom_fields != None:
        for field in config.static_custom_fields.keys():
            api.set_custom_field(id, field, config.static_custom_fields[field])

    for translation in config.translations:

        #INIT
        hits=[]

        #SOURCE
        if translation['source_type'] == "MILESTONE" and issue.milestone != None:
            match = translation['match_object'].search(issue.milestone)
            if match:
                hits.append(match)

        if translation['source_type'] == "LABEL":
            for ilabel in issue.labels:
                match = translation['match_object'].search(ilabel)
                if match:
                    hits.append(match)

        #DEST
        for match in hits:
            if match and len(match.groups()) > 0:
                source_group=match.group(1)
            else:
                source_group=None

            print " => Translation [%s (%s)=>%s (%s, %s)]"%(translation['source_type'], translation['match_object'].pattern,translation['destination_type'], str(translation['destination_opts']),source_group)

            if translation['destination_type'] == "CUSTOM_FIELD":
                ( field_name, field_value ) = translation['destination_opts']
                if source_group != None:
                    value = field_value % (source_group)
                else:
                    value = field_value
                api.set_custom_field(id, field_name, value)

            if translation['destination_type'] == "APPEND_CUSTOM_TEXT_FIELD":
                ( field_name, field_value ) = translation['destination_opts']
                if source_group != None:
                    value = field_value % (source_group)
                else:
                    value = field_value
                task_info = api.get_task_info(id)
                aux_field_name="std:maniphest:%s"%(field_name)
                if task_info['auxiliary'].has_key(aux_field_name) and task_info['auxiliary'][aux_field_name] != None:
                        value = task_info['auxiliary'][aux_field_name] + ", " + value
                api.set_custom_field(id, field_name, value)

            if translation['destination_type'] == "SET_PROJECT":
                new_project = translation['destination_opts']
                new_project_phid = api.get_project_phid(new_project)
                api.change_project(id, [new_project_phid])

            if translation['destination_type'] == "ADD_PROJECT":
                new_project = translation['destination_opts']
                new_project_phid = api.get_project_phid(new_project)
                projects=set(api.get_task_info(id)['projectPHIDs'])
                new_projects=list(projects.union([new_project_phid]))
                api.change_project(id, new_projects)

            if translation['destination_type'] == "COMPONENT":
                field_name = translation['destination_opts']
                component_name = field_name + ":" + lower_snake_caseify(source_group)
                api.set_custom_field(id, field_name, component_name)

            if translation['destination_type'] == "STATUS":
                field_value = translation['destination_opts']
                api.set_status(id, field_value)

            if translation['destination_type'] == "PRIORITY":
                field_value = translation['destination_opts']
                api.set_priority(id, field_value)


    for (author, date, comment) in issue.comments:
        print "Adding comment from %s" % author
        author_phid = api.get_phid_by_username(author)
        if author_phid is None or config.have_db_access is False:
            comment = "> Comment originaly made by **%s** on //%s//\n\n%s" % (author, date, comment)
        # Migrate Attachments
        m_attachment = re_attachment.search(comment)
        while m_attachment != None:
            s_pos = m_attachment.start(0)
            e_pos = m_attachment.end(0)
            print " => Attachment Found: \"%s\"" % (comment[s_pos:e_pos])
            title = m_attachment.group(1)
            link = m_attachment.group(2)
            try:
                data = urllib2.urlopen (link)
            except urllib2.HTTPError, e:
                comment = comment[0:s_pos] + "** FAILED TO MIGRATE <%s|%s> **"%(title, link) + comment[e_pos:-1]
            else:
                upload = api.upload_file(title, data.read(), "")
                comment = comment[0:s_pos] + "{%s}"%upload["objectName"] + comment[e_pos:-1]
            m_attachment = re_attachment.search(comment)
        api.task_comment(id, comment)
        if config.have_db_access:
            tphid = phabdb.last_comment(phid)
            phabdb.set_comment_time(tphid, date.strftime("%s"))
            if author_phid:
                phabdb.set_comment_author(tphid, author_phid)

util.purge_cache()
