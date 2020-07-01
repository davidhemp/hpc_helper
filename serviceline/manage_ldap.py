import ldap3
from ldap_key import *

managed_groups = ["jfAccessToIridis4", 
                    "jfAccessToIridis5", 
                    "jfAccessToLyceum4",
                    "jfAccessToLyceum5"]


def connect():
    return conn

def add_member(group, user):
    server = ldap3.Server("SRV00369.soton.ac.uk", get_info=ldap3.ALL)
    conn = ldap3.Connection(server, ldap_user, ldap_password, auto_bind=True)
    if group not in managed_groups:
        print("Unknown managed group: ".format(group))
    else:
        required_filter = "(&(objectclass=group)(cn={}))".format(group)
        rtn = conn.search("dc=soton,dc=ac,dc=uk", required_filter)
        if rtn:
            group_dn = conn.entries[0].entry_dn
            required_filter = "(&(objectclass=user)(cn={}))".format(user)
            rtn = conn.search("dc=soton,dc=ac,dc=uk", required_filter)
            if rtn:
                user_dn = conn.entries[0].entry_dn
                conn.extend.microsoft.add_members_to_groups(user_dn, group_dn)

def get_all_members():
    server = ldap3.Server("SRV00369.soton.ac.uk", get_info=ldap3.ALL)
    conn = ldap3.Connection(server, ldap_user, ldap_password, auto_bind=True)
    current_users = dict()
    for cluster in managed_groups:
      search_filter="(memberOf=CN={},OU=resource,OU=jf,OU=jf,OU=pk,OU=User,DC=soton,DC=ac,DC=uk)".format(cluster)
      conn.search("dc=soton,dc=ac,dc=uk", search_filter, attributes=["cn"])
      current_users[cluster] = [entry.cn.value for entry in conn.entries]
    return current_users    
