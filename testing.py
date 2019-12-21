import server, device, task, apiconfig, utility






ep1 = device.Endpoint()
ep1.install_progress(1,6,2)
ep1.install_progress(5,100,2)

ep1.ep_register()
ep1.ep_clntstrd()
cmd = server.Commands()
sasids = []
sasids.append(ep1.sas_id)

dct_task = cmd.crt_wl_scan(sasids)

ep1.ep_get_task()

ep1.task.wl_scan_start()
ep1.task.wl_scan_done()
ep1.task.wl_upload()

'''
my_json = '{"user":"vignesh", "dept":"123.234",' \
          ' "attendance":[{"jan":"25","feb":22,"mar":28, "apr":26, "may":25, "jun":24}, "123"]}'


my_schema = '{"type":"object", "properties":{"policy": {"type":"object", "properties":{"header":{"type":"object", "properties":{"force":{"type":"number"}}}, "scanner":{"type":"object", "properties":{"updtcmdarg":{"type":"string"}}},"gnrl":{"type":"object", "properties": {"notifyusr":{"type":"number"}, "alrtusr":{"type":"number"}, "showsystray":{"type":"number"}, "usercanuninstall":{"type":"number"}}},"devicectrl":{"type":"object", "properties":{"on":{"type":"number"}, "ntfyonly":{"type":"number"}, "msg":{"type":"null"}, "hwblock":{"type":"array", "items":{"type":"object", "properties":{"type":{"type":"number"}, "name":{"type":"string"}, "label":{"type":"string"}}}}, "hwallow":{"type":"array", "items":{"type":"object", "properties":{"type":{"type":"number"}, "name":{"type":"string"}, "label":{"type":"string"}}}}}},"execctrl":{}, "fwappctrl":{}, "sandbox":{}, "override":{}}}}}'


with open('c:\\users\\vignesh\\desktop\\e3f.txt', 'r') as h_schema_plcy:
    schema_plcy = json.load(h_schema_plcy)

with open('default_policy.json','r') as h_json:
    d_policy_json = json.load(h_json)

#print(schema_plcy)
print(jsonschema.validate(d_policy_json,json.loads(my_schema)))
'''