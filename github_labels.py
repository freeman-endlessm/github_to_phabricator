#!/usr/bin/python

import json
from config import *
from github_cache import *

class Label(object):
    def __init__(self, github_dict):
        self.json = github_dict
        self.url = self.json['url']
        self.name = self.json['name']
        self.color = self.json['color']

def FetchGithubLabels():
    page = 1
    num_pages = 1
    labels = []
    github_labels = []

    while page <= num_pages:
        (headers, labels_json) = fetch_json("/repos/%s/%s/labels?state=all&per_page=100&page=%d" % (USER, PROJECT, page))
        page = page + 1
        labels.extend(json.loads(labels_json))
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

    for i in labels:
        label = Label(i)
        github_labels.append(label)

    return sorted(github_labels)


if __name__ == '__main__':
    custom_field_definitions={}
    label_matches = {}
    for field_name in LABELS_TO_FIELDS.keys():
        custom_field_definitions[LABELS_TO_FIELDS[field_name]["PHABRICATOR_FIELD"]] = {
          "name": field_name,
          "description": field_name,
          "type": "select",
          "options": {},
          "search": True,
          "fulltext": True
        }
        label_matches[field_name] = re.compile(LABELS_TO_FIELDS[field_name]["GITHUB_LABEL_PATTERN"])

    label_map={}

    labels = FetchGithubLabels()
    for label in labels:
        for field_name in LABELS_TO_FIELDS.keys():
            m = label_matches[field_name].match(label.name)
            if m:
                suffix_name = m.group(1)
                field_id=LABELS_TO_FIELDS[field_name]["PHABRICATOR_FIELD"]
                option_id="%s-%s"%(field_id,suffix_name.lower().replace(" ", "-"))
                print "Got %s: %s"%(field_name, suffix_name)
                custom_field_definitions[field_id]["options"][option_id]=suffix_name
                label_map[label.name]=[field_name, option_id]
    print "\n\nCustom Field Definitions:\n---"
    print json.dumps(custom_field_definitions)
    print "---\n\nLabel Translation Config:\n---"
    print json.dumps(label_map)
