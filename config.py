#!/usr/bin/python

import re

## Main Config
USERNAME="github username"
TOKEN="github access token"
USER="organization"
PROJECT="repository"
MIN_ID=None
MAX_ID=None

#github_members.py
CREATE_ACCOUNTS=True
ACCOUNT_EMAIL_DOMAIN="domain.com"

BASE_URL="https://api.github.com"
CACHE_DIR="cache/"

STATIC_FIELDS="""
    "com.example.task_type": {
        "name": "Type",
        "description": "Task Type",
        "type": "select",
        "options": {
            "com.example.task_type:none": "",
            "com.example.task_type:bug": "Bug",
            "com.example.task_type:enhancement": "Enhancement",
            "com.example.task_type:feature": "Feature"
        },
        "search": true
    },
    "com.example.release": {
       "name": "Release",
       "description" : "release version",
       "type": "select",
       "options": {
           "com.example.release:none": "",
           "com.example.release:1.0.0": "1.0.0",
           "com.example.release:1.0.1": "1.0.1",
           "com.example.release:1.0.2": "1.0.2",
           "com.example.release:1.0.3": "1.0.3",
           "com.example.release:1.0.4": "1.0.4",
           "com.example.release:1.1.0": "1.1.0",
           "com.example.release:1.2.0": "1.2.0"
       },
       "search": true
    },
    "com.example.team" : {
       "name": "Team",
       "description": "Responsible development team",
       "type": "select",
       "options": {
          "com.example.team:none": "",
          "com.example.team:apps": "Apps",
          "com.example.team:core": "Core",
          "com.example.team:services": "Services"
       },
       "search": true
    },
    "com.example.component" : {
       "name": "Component",
       "description": "Software Component",
       "type": "select",
       "options": {
          "com.example.component:none": "",
          "com.example.component:audio_video": "Audio / Video",
          "com.example.component:build_infrastructure": "Build Infrastructure",
          "com.example.component:content": "Content",
          "com.example.component:core_platform": "Core Platform",
          "com.example.component:desktop": "Desktop",
          "com.example.component:dev_tools": "Dev Tools",
          "com.example.component:file_manager": "File Manager",
          "com.example.component:games": "Games",
          "com.example.component:help_center": "Help Center",
          "com.example.component:initial_setup": "Initial Setup",
          "com.example.component:localization": "Localization",
          "com.example.component:peripherals": "Peripherals",
          "com.example.component:power_boot": "Power / Boot",
       },
       "search": true
    },
    "com.example.hw_product": {
        "name": "HW Product",
        "description": "Specific hardware model(s) (if applicable)",
        "type": "text",
        "search": true
    }
"""

## Strip the following patterns from issue descriptions
CLEAN_DESCRIPTION_REGEXES=[
    re.compile("<!--.*?huboard.*?-->\n?", re.MULTILINE | re.DOTALL),
]
