#!/usr/bin/env python

#Phabricator API Access Settings:
phab_token = "api-token"
phab_host = "https://phabricator.example.com/api/"
phabricator_path = "/srv/phabricator"

#phabricator DB access Settings:
have_db_access = True #Disabling this setting is untested and will likely break lots of stuff now...
force_ids = False
delete_existing_issues = False
dbhost = "localhost"
phuser_user = "root"
phuser_passwd = "password"

#Migration Settings:
migration_user = "github-migration" #Phabricator Migration User
project_name = "project-name" #Default Project to add tasks to
static_custom_fields = { "com.example.team": "com.example.team:core" } #Default cutom fields to set on all tasks
file_upload_timeout = 300

##
## Translations
##   use source data from github to effect the task import. See examples
## below. translations are run on every task in order. later translations
## can override what earlier translations have done.
##
##

import re
translations = [
  {
    "source_type":      "MILESTONE",
    "match_object":     re.compile("^Version-(\d+\.\d+\.\d+)"),
    "destination_type": "CUSTOM_FIELD",
    "destination_opts": [ "com.example.release", "com.example.release:%s" ]
  },
  {
    "source_type":      "MILESTONE",
    "match_object":     re.compile("^(?:Closed )?IT Tasks"),
    "destination_type": "SET_PROJECT",
    "destination_opts": "IT",
  },
  {
    "source_type":      "MILESTONE",
    "match_object":     re.compile("^(?:Closed )?IT Tasks"),
    "destination_type": "CUSTOM_FIELD",
    "destination_opts": [ "com.example.team", "com.example.team:none" ],
  },
  {
    "source_type":      "LABEL",
    "match_object":     re.compile("^Critical$"),
    "destination_type": "PRIORITY",
    "destination_opts": 100
  },
  {
    "source_type":      "LABEL",
    "match_object":     re.compile("^High Priority$"),
    "destination_type": "PRIORITY",
    "destination_opts": 80
  },
  {
    "source_type":      "LABEL",
    "match_object":     re.compile("^Medium Priority$"),
    "destination_type": "PRIORITY",
    "destination_opts": 50
  },
  {
    "source_type":      "LABEL",
    "match_object":     re.compile("^Low Priority$"),
    "destination_type": "PRIORITY",
    "destination_opts": 25
  },
  {
    "source_type":      "LABEL",
    "match_object":     re.compile("^Unprocessed$"),
    "destination_type": "PRIORITY",
    "destination_opts": 90
  },
  {
    "source_type":      "LABEL",
    "match_object":     re.compile("^Cmpnt:\w*(.+)$"),
    "destination_type": "COMPONENT",
    "destination_opts": "com.example.component",
  },
  {
    "source_type":      "LABEL",
    "match_object":     re.compile("^Product:\w*(.+)$"),
    "destination_type": "APPEND_CUSTOM_TEXT_FIELD",
    "destination_opts": [ "com.example.hw_product", "%s" ],
  },
  {
    "source_type":      "LABEL",
    "match_object":     re.compile("^(:?Duplicate|Invalid)$"),
    "destination_type": "STATUS",
    "destination_opts": "invalid",
  },
  {
    "source_type":      "LABEL",
    "match_object":     re.compile("^Won't fix$"),
    "destination_type": "STATUS",
    "destination_opts": "wontfix",
  },
  {
    "source_type":      "LABEL",
    "match_object":     re.compile("^Bug$"),
    "destination_type": "CUSTOM_FIELD",
    "destination_opts": [ "com.example.task_type", "com.example.task_type:bug" ],
  },
  {
    "source_type":      "LABEL",
    "match_object":     re.compile("^Enhancement$"),
    "destination_type": "CUSTOM_FIELD",
    "destination_opts": [ "com.example.task_type", "com.example.task_type:enhancement" ],
  },
  {
    "source_type":      "LABEL",
    "match_object":     re.compile("^Blocked: Product$"),
    "destination_type": "ADD_PROJECT",
    "destination_opts": "Product",
  },
  {
    "source_type":      "PHAB_COMPONENT",
    "match_object":     re.compile(":(?:database|infrastructure)$"),
    "destination_type": "CUSTOM_FIELD",
    "destination_opts": [ "com.example.team", "com.example.team:services" ],
  },
]
