import requests, json, utility, apiconfig


class Commands():
    def __init__(self, url=None, uname= None, upwd= None):
        self.API = apiconfig.AppSettings()
        self.token = None
        if url == None:
            url = self.API.API_WEB_LGN

        log_headers = {'content-type': 'application/json'}

        if uname== None or upwd == None:
            uname = self.API.USER
            upwd =  self.API.PWD

        log_data = {'uname': uname, 'upwd': upwd, 's': 1}
        resp = requests.post(url, json=log_headers, data=log_data)

        if resp.status_code == 200:
            resp_json = json.loads(resp.text)
            self.token = 'Bearer ' + (resp_json['token'])

    def crt_wl_scan(self, sas_ids):
        ts = utility.get_time()
        url = self.API.API_WEB_NEWTSK
        hdr =  {'content-type': 'application/json', 'Authorization': self.token}
        params = {'action':'add','t':ts}
        tsk_name = "auto_wl_"+ts

        wl_scn_tsk = {"chunk":'{"type":50,"id":'+ts+',"name":"","scan_rpt_type":1}',
                      "tsk_name":tsk_name, "tsk_type":50, "tsk_guid":ts, "stype":1, "cmp":sas_ids}

        resp = requests.post(url, headers=hdr, params=params, json=wl_scn_tsk)
        if resp.status_code == 200:
            d = dict()
            d['sas_ids']=sas_ids
            d['task_type'] = 50
            d['task_name']=tsk_name
            d['task_id']=json.loads(resp.text)["task_guid"]
            return d

        return None

    def crt_enbl_prot(self, sas_ids):
        ts = utility.get_time()
        url = self.API.API_WEB_NEWTSK
        hdr = {'content-type': 'application/json', 'Authorization': self.token}
        params = {'action': 'add', 't': ts}
        tsk_name = "auto_enb_"+ts
        sts = "1001-5-0"

        enbl_prot = {"chunk":'{"type":15,"id":'+ts+',"name":"","compsts": sts}',
                     "tsk_name": tsk_name,"tsk_type":15,"tsk_guid":ts,"stype":1,"cmp":sas_ids}

        resp = requests.post(url, headers=hdr, params=params, json=enbl_prot)
        if resp.status_code == 200:
            d = dict()
            d['sas_ids'] = sas_ids
            d['task_id'] = json.loads(resp.text)["task_guid"]
            d['task_type'] = 15
            d['task_name'] = tsk_name
            d['cmp_sts'] = sts
            return d

        return None

    def crt_dsbl_prot(self, sas_ids):
        print(sas_ids)
        ts = utility.get_time()
        url = self.API.API_WEB_NEWTSK
        hdr = {'content-type': 'application/json', 'Authorization': self.token}
        params = {'action': 'add', 't': ts}
        tsk_name = "auto_enb_"+ts
        sts = "1001-6-0"

        enbl_prot = {"chunk": '{"type":15,"id":' + ts + ',"name":"","compsts": sts}',
                     "tsk_name": tsk_name, "tsk_type": 15, "tsk_guid": ts, "stype": 1, "cmp": sas_ids}

        resp = requests.post(url, headers=hdr, params=params, json=enbl_prot)
        if resp.status_code == 200:
            d = dict()
            d['sas_ids'] = sas_ids
            d['task_id'] = json.loads(resp.text)["task_guid"]
            d['task_type'] = 15
            d['task_name'] = tsk_name
            d['cmp_sts'] = sts
            return d

        return None