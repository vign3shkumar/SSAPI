import json
'''
global API_INSTL_PRGS
global API_DVC_REGISTER
global API_DVC_CLNTSTRD
global API_DVC_PLCY
global API_DVC_HB
global API_DVC_PSC
global API_DVC_TSK
global API_DVC_STL
global API_DVC_UPLD
global API_DVC_DWLD
global API_WEB_LGN
global API_WEB_NEWTSK

server = "http://172.16.3.181"
api_path = "/api/v1/"
server= server+api_path
API_INSTL_PRGS = server+"device/installprogress"
API_DVC_REGISTER = server+"device/register"
API_DVC_CLNTSTRD = server+ "device/clntstrd"
API_DVC_PLCY = server+"device/getpolicy"
API_DVC_HB = server+ "device/pulse"
API_DVC_PSC = server+"device/protchng"
API_DVC_TSK = server+"device/getask"
API_DVC_STL = server+ "device/statuslog"
API_DVC_UPLD = server+"device/wlupldinfo"
API_DVC_DWLD = server+"device/getwldbinfo"
API_WEB_LGN = server+"user/login"
API_WEB_NEWTSK = server+"task/create"
'''


class AppSettings:

    def __init__(self, scpt_environment = None):
        with open('config.json', 'r') as h_script_config:
            script_config = json.load(h_script_config)

        if scpt_environment is None:
            scpt_environment='qa'

        server = script_config[scpt_environment]['server']+script_config[scpt_environment]['api_path']

        self.API_INSTL_PRGS = server+script_config[scpt_environment]['install_progress']

        self.API_DVC_REGISTER = server+script_config[scpt_environment]['register']

        self.API_DVC_CLNTSTRD= server+script_config[scpt_environment]['clntstrtd']

        self.API_DVC_PLCY = server+script_config[scpt_environment]['getplcy']

        self.API_DVC_HB = server+script_config[scpt_environment]['pulse']

        self.API_DVC_PSC = server+script_config[scpt_environment]['protchng']

        self.API_DVC_TSK = server+script_config[scpt_environment]['get_task']

        self.API_DVC_STL = server+script_config[scpt_environment]['sts_log']

        self.API_DVC_UPLD = server+script_config[scpt_environment]['wlupld_info']

        self.API_DVC_DWLD = server+script_config[scpt_environment]['get_wldb']

        self.API_WEB_LGN = server+script_config[scpt_environment]['login']

        self.API_WEB_NEWTSK = server+script_config[scpt_environment]['crt_task']

        self.USER = script_config[scpt_environment]['user']

        self.PWD = script_config[scpt_environment]['pwd']


