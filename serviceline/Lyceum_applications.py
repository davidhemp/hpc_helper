from datetime import datetime, timedelta
import subprocess

import pysnow

#Password and user are kept seperate.
from hpc_key import *

import manage_ldap

client = pysnow.client.Client(host='sotonproduction.service-now.com',
                              user=sl_user, password=sl_password)

request = client.resource(api_path='/v1/table/sc_req_item')
form_request = client.resource(api_path='/uno49/ritm_iridis_api', base_path='/api')
user_request = client.resource(api_path='/v1/table/sys_user')

lower_limit = datetime.today() - timedelta(days=7)
query = pysnow.QueryBuilder() \
        .field('short_description').starts_with('Lyceum Account Application') \
        .AND().field('sys_created_on').greater_than(lower_limit)

response = request.get(query=query, stream=True)

current_users = manage_ldap.get_all_members()

for record in response.all():
    if record['assigned_to'] != '':
        # Only check tickets assigned to dwh1d17 and "in progress" state
        if record['assigned_to']['value'] == '68e65aaedbb6c70014367db33c961998' and record["state"] == "2":
            ritm = record['number']
            print("----")
            print(ritm)
            variables = form_request.request('GET', headers={"ritm": ritm}).one()[ritm]
            if len(variables["lyceum_additional"]) > 0:
                print("Supervisor has additional comments.")
                print(variables["lyceum_additional"])
            for i in range(1, int(variables["lyceum_number"])+1):
                userid = variables["lyceum_name_{}".format(i)]
                # We now add users to both clusters
                clusters = ["jfAccessToLyceum5", "jfAccessToLyceum4"]
                user = user_request.get(query={'sys_id': userid})
                user = user.one()
                if user["user_name"] != "":
                    for cluster in clusters:
                        if user['user_name'] in current_users[cluster]:
                            print("{} is already in group {}.".format(user["user_name"], cluster))
                        else:
                            print("Adding: {} to {}.".format(user["user_name"], cluster))
                            manage_ldap.add_member(cluster, user["user_name"])
                else:
                    print("ERROR: User has no username assigned!")
