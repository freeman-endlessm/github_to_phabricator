import base64
import config
import phabricator
import traceback
from phabricator import Phabricator
from phabricator import Resource
import phabdb
import time
from util import log
from util import vlog
from util import errorlog as elog

class phabapi:
    """wrapper for phab api"""

    def __init__(self):
        self.con = Phabricator(host=config.phab_host, token=config.phab_token)

    def call_method(self, method, endpoint, args):
	retries = 2
	out = None
        __method = Resource(api=self.con, method=method, endpoint=endpoint)
	while out == None and retries > 0:
	    try:
		out = __method(**args)
	    except Exception, e:
		print "Warning: API Call to %s.%s with args %s failed:\n%s" % (method, endpoint, args, e)
		traceback.print_exc()
		time.sleep(1)
		retries = retries - 1
	if out == None:
	    raise Exception("API Call to %s.%s failed 3 times, giving up..."%(method, endpoint))
        return out

    def task_comment(self, task, msg):
        out = self.call_method("maniphest", "update", {'id': task, 'comments': msg})
        return out

    def set_status(self, task, status):
        out = self.call_method("maniphest", "update", {'id': task, 'status': status})
        return out

    def set_priority(self, task, priority):
        out = self.call_method("maniphest", "update", {'id': task, 'priority': priority})
        return out

    def set_custom_field(self, task, field, value):
        out = self.call_method("maniphest", "update", {'id': task, 'auxiliary': {"std:maniphest:%s"%(field): value}})
        return out

    def change_project(self, task, projects=[]):
        out = self.call_method("maniphest", "update", {'id': task, 'projectPHIDs': projects})
        return out

    def get_task_info(self, task):
        out = self.call_method("maniphest", "info", {'task_id': int(task)})
        return out

    def task_create(self, title, desc, id, priority, ownerPhid=None, projects=[]):
	return self.call_method( "maniphest", "createtask",
	    {
		'title': title,
		'description': desc,
		'projectPHIDs': projects,
		'priority': priority,
		'ownerPHID': ownerPhid,
		'auxiliary': {"std:maniphest:external_reference":"%s" % (id,)}
	    })

    def get_project_phid(self, name):
        result = self.call_method("project", "query", {'names': [name]})
        if result:
            return result['data'].keys()[0]
        return None

    def get_phid_by_username(self, username):
        result = self.call_method("user", "query", {'usernames': [username]})
        if len(result.response):
            return result[0]['phid']
        return None

    def create_user(self, username, realname, email, password):
        self.call_method("user", "create", {'username': username, 'realname': realname, 'email': email, 'password': password})
	# should this return something?

    if config.have_db_access:
        def ensure_project(self, project_name,
                                 pmembers=[],
                                 view='public',
                                 edit='public'):
            """make sure project exists
            :param project_name: str
            :param pmembers: list
            :param view: str
            :param edit str"""
            existing_proj = phabdb.get_project_phid(project_name)
            #print "EXISTING PROJ: ", existing_proj
            #print "EXISTING PROJ TYPE: ", type(existing_proj)
            #existing_proj = self.con.project.query(names=[project_name])
            if not existing_proj:
                log('need to create project(s) ' + project_name)
                try:
                    new_proj = self.con.project.create(name=project_name, members=pmembers)
                #XXX: Bug where we have to specify a members array!
                except phabricator.APIError:
                    pass
                phid = phabdb.get_project_phid(project_name)
                if not phid:
                    raise Exception("Project %s does not exist still." % (project_name,))
                #existing_proj = self.con.project.query(names=[project_name])
                #log(str(existing_proj))
                #phid = existing_proj['data'][existing_proj['data'].keys()[0]]['phid']
                phabdb.set_project_policy(phid, view, edit)
            else:
                phid = existing_proj
                #phid = existing_proj['data'][existing_proj['data'].keys()[0]]['phid']
                log(project_name + ' exists')
            return phid

        def upload_file(self, name, data, viewPolicy, dump=False):

            if dump:
                with open(name, 'wb') as f:
                    f.write(data)

            log("upload policy for %s is %s" % (name, viewPolicy))
            out = {}
            self.con.timeout = config.file_upload_timeout
            chunk_threshold = 8*1024*1024;
            chunk_size = 4*1024*1024;
            file_len = len(data)
            if file_len <= chunk_threshold:
                encoded = base64.b64encode(data)
                response = self.call_method("file", "upload", {'name': name, 'data_base64': encoded, 'viewPolicy': viewPolicy})
		uploadphid = response.response
                out['phid'] = uploadphid
            else: # Do chunked upload
                uploadphid = self.call_method("file", "allocate", {'name': name, 'contentLength': file_len, 'viewPolicy': viewPolicy})['filePHID']
		cur_pos = 0
		while cur_pos < file_len:
		    end_pos = cur_pos + chunk_size
		    encoded=base64.b64encode(data[cur_pos:end_pos])
		    self.call_method("file", "uploadchunk", {'filePHID': uploadphid, 'byteStart': cur_pos, 'dataEncoding': "base64", 'data': encoded})
		    cur_pos = end_pos
                out['phid'] = uploadphid
            log("%s upload response: %s" % (name, uploadphid))
            fileid = phabdb.get_file_id_by_phid(uploadphid)
            out['id'] = int(fileid)
            out['name'] = name
            out['objectName'] = "F%s" % (fileid,)
            log("Created file id: %s" % (fileid,))
            self.con.timeout = 5
            return out

        def ticket_id_by_phid(self, phid):
             tinfo = self.con.maniphest.query(phids=[phid])
             if not tinfo:
                 return ''
             if not tinfo.keys():
                 return ''
             return tinfo[tinfo.keys()[0]]['id']
