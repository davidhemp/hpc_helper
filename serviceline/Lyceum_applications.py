from datetime import datetime, timedelta
import subprocess

import pysnow

#Password and user are kept seperate. 
from hpc_key import *

with open("/home/dwh1d17/.ssh/admdh.key") as f:
    admdh_passwd = f.read().strip("\n")
adcli = "/mainfs/home/dwh1d17/tools/hpc_helper/serviceline/adcli.sh"

client = pysnow.client.Client(host='sotonproduction.service-now.com',
                              user=user, password=password)

request = client.resource(api_path='/v1/table/sc_req_item')
form_request = client.resource(api_path='/uno49/ritm_iridis_api', base_path='/api')
user_request = client.resource(api_path='/v1/table/sys_user')

lower_limit = datetime.today() - timedelta(days=7)
query = pysnow.QueryBuilder() \
        .field('short_description').starts_with('Lyceum Account Application') \
        .AND().field('sys_created_on').greater_than(lower_limit)

#response = request.get(query=query, stream=True)
response = request.get(query={'number':'RITM0204120'})

for record in response.all():
    ritm = record['number']
    print("----")
    print(ritm)
    variables = form_request.request('GET', headers={"ritm": ritm}).one()[ritm]
    try:
        if len(variables["lyceum_additional"]) > 0:
            print("Supervisor has additional comments.")
            print(variables["lyceum_additional"])
            continue
    except KeyError:
        pass
    for i in range(1, int(variables["lyceum_number"])+1):
        userid = variables["lyceum_name_{}".format(i)]
        try:
            if variables["lyceum_gpu_{}".format(i)][0] == "Y":
                cluster = "jfAccessLyceum5"
            else:
                cluster = "jfAccessLyceum4"
        except KeyError:
            cluster = "jfAccessLyceum4"
        user = user_request.get(query={'sys_id': userid})
        username = user.one()["user_name"]
        print(username, cluster)
        subprocess.call(["echo", "{}".format(admdh_passwd), ">", "adcli", "add-member", "--stdin-password", "-D", "soton.ac.uk", "-U", "admdh", cluster, username], shell=True)
        #subprocess.call([adcli, admdh_passwd, cluster, username], shell=True)
