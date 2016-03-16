Github to Phabricator migration tool
---

# Requirements
You will need python, python-phabricator, and python-mysqld.
You will also need to have 'curl' installed.
You will need local access to the phabricator installation as well as database access.

# Fetching from github
This tool has three parts, the first is what fetches all of data from github,
you can configure it in ./config.py by setting the username, api token (that you generate in settings->personal access token), the project's org and repository name.
You can also set a minimum and maximum issue id to fetch for the migration. 
The data that gets downloaded from github is cached, so you must create a cache directory before use. If you want to refresh the issues, simply delete its content.
The script uses the external command 'curl' to fetch all the data, so make sure curl is installed. You can run ./github_issues.py to get it to fetch the issues and comments and print out the title and id of all the issues it found.

# Preparing Phabricator
The second part creates a bunch of users based on members of your github organization, so the migration can preserve as much audit history as possible.
You must provide a mapping of github username to your organizations username and real name (see user_map.csv.ex.)
Important settings in ./config.py are (CREATE_ACCOUNTS and ACCOUNT_EMAIL_DOMAIN)
*NOTE:* Phabricator does not provide an API endpoint for creating users, one is included in contrib/phabricator_extensions/.
Your migration user must be a phabricator administrator to hit this endpoint.

# Importing into Phabricator
The second part is what uploads the data to Phabricator. It can be configured in wmfphablib/config.py file. It will need a dedicated user for the migration (by default "github-migration"), so you must create such a user (add -> User Account) and set it as a bot.
You will then need to generate a conduit API token for that user, by accessing the user's profile (you can search for the user github-migration, then Edit settings, then Conduit API token).
Once you generate the token, you can set the phabricator URL, install path, databaser user/password and the Conduit token in the wmfphablib/config.py file.
Setting the phabricator_path is only necessary if you want to delete the existing tasks before importing. If `delete_existing_issues` is set to `False`, then the phabricator_path and access to the server is not required. Deleting existing tasks will only delete the tasks for the selected project, to avoid any potential mistakes.

# Translate Labels
There is a complex system of "translations" that can happen during the migration.
This allows you to use github labels and milestones to set Phabricator tasks during
the migration. set priority, status, custom fields, even add or replace destination
project tags. It is not well documented, but some examples are provided in the
wmfphablib/config.py file. It most certainly conatins bugs ;-)

# License
The wmfphablib code was copied from the wikimedia phabricator tools repository (https://gerrit.wikimedia.org/r/#/admin/projects/phabricator/tools) and modified to suit our needs.
This tool is therefore released under the same license as wikimedia's phabricator tools : GPL v2. See the LICENSE file for more information.
