import wlcreate, requests, utility, os, apiconfig
from requests import Request, Session


'''
 task types
   50 - Whitelist scan
   51 - Check Hardening status
   9  - Uninstall task
   15 - change protection
'''
class Task():
    def __init__(self, sas_id, task_id, task_type, task_name= None, tsk_compsts= None):
        self.taskid = task_id
        self.task_type = task_type
        self.task_name = task_name
        self.task_comp_status =  tsk_compsts
        self.status_log_param = None
        self.ep_repo = utility.createDir("WLRepo\\"+sas_id, True)
        self.scan_wlfile = None
        self.sas_id = sas_id
        self.API = apiconfig.AppSettings()

    def status_log(self):
        self.status_log_param = {"type":1,"status":1,"errorcode":"","task_id":self.taskid}
        jsondata = {"sas_id":self.sas_id, "status_blob":self.status_log_param}
        s_headers = {'content-type': 'application/json'}
        requests.post(self.API.API_DVC_STL, headers=s_headers, json=jsondata)

    def wl_scan_start(self):
        self.status_log_param = {"type":1, "status":1, "errorcode":"", "task_id":self.taskid}
        self.status_log()
        wlcreate.create_scanhashinfo(self.ep_repo)


    def wl_scan_done(self):
        self.scan_wlfile = wlcreate.compress_file(self.ep_repo, self.ep_repo)
        self.status_log_param = {"type": 1, "status": 3, "errorcode": "", "task_id": self.taskid}
        self.status_log()

    def wl_scan_error(self):
        self.status_log_param = {"type": 1, "status": 2, "errorcode": "An error occurred during scan task", "task_id": self.taskid}
        self.status_log()

    def wl_upload(self):
        self.status_log_param = {"type": 3, "status": 1, "errorcode": "", "task_id": self.taskid}
        self.status_log()

        fl_size = os.stat(self.scan_wlfile).st_size
        upld_hdr = {'content-type':'application/octet-stream', 'content-length':str(fl_size)}

        params = {'sas_id': self.sas_id, 'TS':utility.get_time(), 'loc':'',
                  'hash_sha256': utility.filename_frmpath(self.scan_wlfile), 'task_id':self.taskid }

        upld_req = Request('POST', self.API.API_DVC_UPLD, headers=upld_hdr, params=params)

        prepped = upld_req.prepare()
        with open(self.scan_wlfile, 'rb') as f:
            prepped.body=(f.read(fl_size))

        s= Session()
        wl_upld_resp = s.send(prepped, stream=True)

        self.status_log_param = {"type": 3, "status": 2, "errorcode": "An error occurred during upload", "task_id": self.taskid}

        if (wl_upld_resp.status_code == 200):
            self.status_log_param = {"type": 3, "status": 3, "errorcode": "", "task_id": self.taskid}
        self.status_log()


    def wl_download(self, sas_id, ver):

        dwld_hdr = {'content-type': 'application/x-form-urlencoded'}
        data = {'sas_id':sas_id}

        dwld_resp = requests.post(self.API.API_DVC_DWLD, dwld_hdr, data)

        if(dwld_resp.status_code == 200):
            wldb_file = self.ep_repo+str(sas_id)+'.zip'
            sha = dwld_resp.headers['X-hash_sha256']
            ver = dwld_resp.headers['X-wlver']
            with open(wldb_file,'wb') as h_wldb:
                h_wldb.write(dwld_resp.content)
        if (sha == utility.get_sha256_file(wldb_file)):
            return ver
        return 0

    def get_compsts(self):
        if self.task_comp_status == '1001-5-0':
            return 1
        return 0
