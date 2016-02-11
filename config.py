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

## Translate GitHub Labels to Phabricator Custom Fields
LABELS_TO_FIELDS = {
  "Component": {
    "PHABRICATOR_FIELD": "com.organization.component",
    "GITHUB_LABEL_PATTERN": "^Component:\s+(.*)"
  },
  "Product": {
    "PHABRICATOR_FIELD": "com.organization.product",
    "GITHUB_LABEL_PATTERN": "^Product:\s+(.*)"
  }
}

STATIC_FIELDS={}

## Strip the following patterns from issue descriptions
CLEAN_DESCRIPTION_REGEXES=[
    re.compile("<!--.*?huboard.*?-->\n?", re.MULTILINE | re.DOTALL),
]
