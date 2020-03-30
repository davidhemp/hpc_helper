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
        .field('short_description').starts_with('Iridis Account Application') \
        .AND().field('sys_created_on').greater_than(lower_limit)

response = request.get(query=query, stream=True)

current_users = manage_ldap.get_all_members()

for record in response.all():
    if record['assigned_to'] != '':
        # Only check tickets assigned to dwh1d17 and "in progress" state
        if record['assigned_to']['value'] == '68e65aaedbb6c70014367db33c961998' and record["state"] == "2":
            user = user_request.get(query={'sys_id': record['u_owner']['value']}, stream=True).first()
            if user["u_type"].lower() in ["pgr", "staff"]:
                ritm = record['number']
                variables = form_request.request('GET', headers={"ritm": ritm}).one()[ritm]
                cluster = variables["choice_of_iridis_service"].replace("hpc_iridis_", "jfAccessToIridis")
                if variables["iridis_filestore_ownership"][0] is not "Y":
                    print("Email user about filestore ownership")
                    continue
                elif variables["iridis_previous_username"][0] is "Y":
                    print("User has a previous username")
                    continue
                else:
                    if user['user_name'] in current_users["jfAccessToIridis4"] or user["user_name"] in current_users["jfAccessToIridis5"]:
                        print("{} is already an Iridis user".format(user["user_name"]))
                    else:
                        experience = variables["iridis_application_user_experience"].split("_")[1]
                        print("Adding: " + " ".join((ritm, user['user_name'], cluster, experience)))
                        manage_ldap.add_member(cluster, user["user_name"])

