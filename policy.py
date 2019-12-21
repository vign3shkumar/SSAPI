import jsonschema, json

class Policy:
    def __init__(self, name=None, plcy_id= None, version=None, chunk=None):
        self.plcy_name = name
        self.plcy_id = plcy_id
        self.plcy_version = version
        self.plcy_chunk= chunk
        self.plcy_id_avail = None
        self.plcy_version_avail = None


    def set_policy(self, plcy_chunk):
        #self.plcy_name = name
        #self.plcy_version = version
        self.plcy_chunk = plcy_chunk

    def set_policy_id(self, plcy_id):
        self.plcy_id = plcy_id

    def set_policy_ver(self, plcy_version):
        self.plcy_version = plcy_version

    def set_available_plcy(self, plcy_id, plcy_version):
        self.plcy_id_avail = plcy_id
        self.plcy_version_avail = plcy_version

    def get_policy(self):
        return self.plcy_chunk

    def get_policy_id(self):
        return self.plcy_id

    def get_policy_ver(self):
        if self.plcy_version == None: return 0
        return self.plcy_version

    def validate_policy(self):

        with open('def_policy_schema.json','r') as h_schema_plcy:
            def_plcy_schema = json.load(h_schema_plcy)

        print(self.plcy_chunk)
        jsonschema.validate(json.loads(self.plcy_chunk), def_plcy_schema)
