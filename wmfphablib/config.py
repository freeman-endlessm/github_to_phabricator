#!/usr/bin/env python
dbhost = "localhost"
phuser_user = "root"
phuser_passwd = "password"
phab_token = "api-token"
phab_host = "https://phabricator.example.com/api/"
phabricator_path = "/srv/phabricator"
project_name = "project-name"
static_custom_fields = { "com.example.team": "com.example.team:core" }
migration_user = "github-migration"
delete_existing_issues = False
force_ids = False
have_db_access = False

file_upload_timeout = 300

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
    "destination_type": "CUSTOM_FIELD",
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
]
