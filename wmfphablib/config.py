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

translate_labels = None
# translate_labels = {
#   #"GitHub Label Name": ("Phabricator Field", "Value"),
#   "P0 - Critical": ("Priority", "100"),
#   "P1 - High Priority": ("Priority", "80"),
#   "P2 - Medium Priority": ("Priority", "50"),
#   "P3 - Low Priority": ("Priority", "25"),
#   # Output from github_labels goes here...
# }
