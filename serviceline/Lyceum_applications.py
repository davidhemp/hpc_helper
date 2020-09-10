from datetime import datetime, timedelta
from time import sleep
import sys

import pysnow

#Password and user are kept seperate.
import hpc_key
import email_users
import manage_ldap

client = pysnow.client.Client(host='sotonproduction.service-now.com',
                              user=hpc_key.sl_user, password=hpc_key.sl_password)

request = client.resource(api_path='/v1/table/sc_req_item')
form_request = client.resource(api_path='/uno49/ritm_iridis_api', base_path='/api')
user_request = client.resource(api_path='/v1/table/sys_user')

lower_limit = datetime.today() - timedelta(days=7)
query = pysnow.QueryBuilder() \
        .field('short_description').starts_with('Lyceum Account Application') \
        .AND().field('sys_created_on').greater_than(lower_limit)

response = request.get(query=query, stream=True)
try:
    records = response.all()
except requests.exceptions.HTTPError:
    print("No Applications found")
    sys.exit()    

current_users = manage_ldap.get_all_members()
for record in response.all():
    if record['assigned_to'] != '':
        # Only check tickets assigned to dwh1d17 and "in progress" state
        if record['assigned_to']['value'] == '68e65aaedbb6c70014367db33c961998' and record["state"] == "2":
            ritm = record['number']
            print("----")
            print(ritm)
            variables = form_request.request('GET', headers={"ritm": ritm}).one()[ritm]
            #The additional comments field is a bit muddled and this is the most reliable way to parse it
            comments = variables['lyceum_additional_1'].split('lyceum_additional:')[1]
            if len(comments) > 0:
                print("Supervisor has additional comments.")
                print(comments)
            for i in range(1, int(variables["lyceum_number"])+1):
                userid = variables["lyceum_name_{}".format(i)]
                # We now add users to both clusters
                clusters = ["jfAccessToLyceum5", "jfAccessToLyceum4"]
                user = user_request.get(query={'sys_id': userid}).one()
                if user["user_name"] != "":
                    email = False
                    for cluster in clusters:
                        if user['user_name'] in current_users[cluster]:
                            print("{} is already in group {}.".format(user["user_name"], cluster))
                        else:
                            print("Adding: {} to {}.".format(user["user_name"], cluster))
                            manage_ldap.add_member(cluster, user["user_name"])
                            email = True
                    if email:
                        print("Sending Welcome email to {} - {}".format(user['name'], user["user_name"]))
                        sender_email = "dwh1d17@soton.ac.uk"
                        receiver_email = "{}@soton.ac.uk".format(user['user_name'])
                        with email_users.connect() as server:
                            msg = email_users.welcome_email(sender_email, receiver_email, user['name'])
                            server.sendmail(sender_email, receiver_email, msg.as_string())
                        print("Email sent. 60 second pause to prevent timeout")
                        sleep(60)

                else:
                    print("ERROR: User has no username assigned!")
                    break
            else:
                #If the for loop exits correctly then the ticket is closed.
                request.update(query={"number":ritm}, payload={"state":3})
                print("Ticket closed")
