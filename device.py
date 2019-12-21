import utility, random, string, requests, name, policy, task, apiconfig

class Device:

    def __init__(self):
        self.t = '1'
        self.ID = utility.get_buildid()
        self.sys_id = utility.get_uuid()
        self.ins_id = utility.get_uuid()
        self.os = self.get_osver()
        self.pcname = self.get_sysname()
        self.dmn = self.get_domain()
        self.mac = self.get_mac()
        self.ram = self.get_ram()
        self.cpu = self.get_cpu()
        self.pctime = utility.get_time()
        self.ip = self.get_ip()
        self.osbtns=random.choice(['32','64'])
        self.sas_id= None
        self.API = apiconfig.AppSettings()



    def get_osver(self):
        return random.choice(['5,1,2600,', '5,2,3790,', '6,0,6002,', '6,0,6003,', '6,1,7600,',
                             '6,1,7601,', '6,1,7601,', '6,2,9200,', '6,3,9600,', '10,0,10240,',
                             '10,0,14393,', '10,0,17763,', '10,0,10586,', '10,0,14393,',
                             '10,0,15063,', '10,0,16299,', '10,0,17134,', '10,0,17763,', '10,0,18362,',
                             '10,0,18363,'])

    def get_sysname(self):
        return random.choice(name.names)+"PC"

    def get_domain(self):
        return random.choice(['ABCCorp', 'WORKGROUP', 'WYSIWYG'])

    def get_mac(self):
        return str(('%064x' % random.randrange(281474976710655))[12:])

    def get_ram(self):
        return random.choice(['2048', '4096', '8192', '9216', '10240', '11264', '12288', '13312', '14336', '15360', '16384'])

    def get_cpu(self):
        return random.choice(['1', '2', '4', '6', '8'])

    def get_ip(self):
        return '.'.join(map(str, (random.randint(10,255) for _ in range(4))))

    def install_progress(self, instl_stage, instl_status, instl_type, instl_error=None):

        install_progress_status = {'cn': self.pcname, 'ip': self.get_ip(), 'st': instl_stage, 's': instl_status,
                                   'e': instl_error, 'i': instl_type, 'id': self.ins_id}

        return requests.get(self.API.API_INSTL_PRGS, params=install_progress_status)


class Endpoint(Device):

    def __init__(self):
        self.prdver = '1.0.1'
        self.Prmlngid = 1
        self.Seclngid = 1
        self.agnt_ver = '1.3'
        self.agent_port = '7077'
        self.contver = '1.0.0011;0.0.0000'
        self.compnt_fwapp = '2001'
        self.compnt_fwnw = '2002'
        self.compnt_fwi = '2003'
        self.compnt_rts = '1001'
        self.compnt_eml = '1002'
        self.compnt_exp = '1003'
        self.compnt_bhv = '1004'
        self.compnts_status ={self.compnt_rts:None, self.compnt_eml:None, self.compnt_exp:None,
                              self.compnt_bhv:None, self.compnt_fwnw:None, self.compnt_fwapp:None,
                              self.compnt_fwi:None}
        self.plcy = policy.Policy()
        self.wlver = None
        self.hdrdngver = None
        super(Endpoint, self).__init__()

    def get_prdver(self):
        return '1.0.101'

    def set_compsts(self, cmpnt, state = None, mod = None):
        if state is None and cmpnt == '1001':
            state = '6'
        elif state is None:
            state='5'
        else:
            state = state

        if mod is None :
            mod = '101'
        else:
            mod = mod

        try:
            self.compnts_status[cmpnt]= cmpnt+'-'+state+'-'+mod
        except :
            print("An invalid state or mod assigned to the method. defaulting state to disabled.")
            self.compnts_status[cmpnt] = cmpnt + '-' + state + '-' + mod

    def set_compsts_clntstrted(self):
        self.set_compsts(self.compnt_rts)
        self.set_compsts(self.compnt_eml)
        self.set_compsts(self.compnt_exp)
        self.set_compsts(self.compnt_bhv)
        self.set_compsts(self.compnt_fwapp)
        self.set_compsts(self.compnt_fwnw)
        self.set_compsts(self.compnt_fwi)

    def turn_off_protection(self):
        return self.set_compsts(self.compnt_rts,6)

    def turn_on_protection(self):
        return self.set_compsts(self.compnt_rts,5)

    def ep_register(self):

        c_reg_headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        self.set_compsts_clntstrted()

        p_ep_register = {'T': self.t, 'Id': self.ID, 'SysID': self.sys_id, 'InsId': self.ins_id,
                          'OsVer': self.os, 'OsPt': '1', 'SysName': self.pcname, 'Domain': self.dmn,
                          'PrdVer': self.prdver, 'mac': self.mac, 'ram': self.ram, 'cpu': self.cpu,
                          'pctime': self.pctime, 'agent_port': self.agent_port}

        reg_response = requests.post(self.API.API_DVC_REGISTER, headers = c_reg_headers, data=p_ep_register)
        self.sas_id = reg_response.headers['SasID']

    def ep_clntstrd(self):
        comps={}
        stats=[]
        c_strd_headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        p_ep_clntstrd = {'sas_id': self.sas_id, 'sysid': self.sys_id, 'insid':self.ins_id, 'port':self.agent_port,
                         'ts': utility.get_time(), 'prdid': self.ID, 'agnt': '1.3', 'sysname': self.pcname, 'os_btns': self.osbtns,
                         'sysdomain': self.get_domain(), 'cpu': self.get_cpu(), 'ram': self.get_ram(), 'Prmlngid': '1',
                         'Seclngid': '1', 'osver': self.get_osver(), 'clientip': self.ip, 'contver': self.contver}

        for stat_val in self.compnts_status.values():
           stats.append(stat_val)
        comps['compsts']=stats

        p_ep_clntstrd.update(comps)

        clnt_strtd_resp = requests.post(self.API.API_DVC_CLNTSTRD, headers=c_strd_headers, data=p_ep_clntstrd)
        return clnt_strtd_resp.text
    
    def ep_setprotchng(self, status, task_id=None):
        c_protchng_headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        prot = self.turn_off_protection()

        if status:
            prot = self.turn_on_protection()

        p_ep_protchng = {'sas_id': self.sas_id, 'compsts': self.prot, 'task_id': task_id}

        clnt_prot_resp = requests.post(self.API.API_DVC_PSC, headers=c_protchng_headers, data=p_ep_protchng)

    def ep_setpolicy(self):

        c_plcy_headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        p_ep_plcy = {'sas_id': self.sas_id, 'pid' : self.plcy.get_policy_ver()}

        clnt_plcy_resp = requests.post(self.API.API_DVC_PLCY, headers=c_plcy_headers, data=p_ep_plcy)
        self.plcy.set_policy(clnt_plcy_resp.text)

    def ep_heartbeat(self):
        c_hb_header = {'Content-Type': 'application/x-www-form-urlencoded'}

        p_ep_hb = {'sas_id':self.sas_id}

        clnt_hb_resp = requests.post(self.API.API_DVC_HB, headers=c_hb_header, data=p_ep_hb)
        self.plcy.plcy_id = clnt_hb_resp.headers['plcyid']
        self.plcy.plcy_version = (clnt_hb_resp.headers['plcyver'])
        clnt_hb_resp.headers['hastask']
        self.wlver = clnt_hb_resp.headers['wlver']

        if 'hrdngver' in clnt_hb_resp.headers:
            self.hdrdngver = clnt_hb_resp.headers['hrdngver']

        #clnt_hb_resp.headers['SrvrTime']

    def ep_get_task(self):
        c_task = {'Content-Type': 'application/x-www-form-urlencoded'}

        p_ep_hb = {'sas_id':self.sas_id}

        clnt_task_resp = requests.post(self.API.API_DVC_TSK, data= p_ep_hb, headers=c_task)

        tsk_props = clnt_task_resp.json()
        for props in (tsk_props['tasks']['list']):
            tsk_id = props['id']
            tsk_name= props['name']
            tsk_type=props['type']
            if tsk_type == 15 :
                self.task = task.Task(self.sas_id, tsk_id, tsk_type, tsk_name, props['compsts'])

            self.task = task.Task(self.sas_id, tsk_id, tsk_type, tsk_name)



    def ep_get_compstschg(self):
            self.ep_setprotchng(self.task.get_compsts(), self.task.taskid)