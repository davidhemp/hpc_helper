import ldap3
from ldap_key import *

def connect():
    server = ldap3.Server("SRV00369.soton.ac.uk", get_info=ldap3.ALL)
    conn = ldap3.Connection(server, ldap_user, ldap_password, auto_bind=True)
    return conn

def add_member(cluster, user):
    conn = connect()
    if cluster not in ["jfAccessToIridis4", "jfAccessToIridis5"]:
        print("Unknown cluster: ".format(cluster))
    else:
        required_filter = "(&(objectclass=group)(cn={}))".format(cluster)
        rtn = conn.search("dc=soton,dc=ac,dc=uk", required_filter)
        if rtn:
            iridis_dn = conn.entries[0].entry_dn
            required_filter = "(&(objectclass=user)(cn={}))".format(user)
            rtn = conn.search("dc=soton,dc=ac,dc=uk", required_filter)
            if rtn:
                user_dn = conn.entries[0].entry_dn
                conn.extend.microsoft.add_members_to_groups(user_dn, iridis_dn)

def get_all_members():
    conn = connect()
    current_users = dict()
    for cluster in ["jfAccessToIridis4", "jfAccessToIridis5"]:
      search_filter="(memberOf=CN={},OU=resource,OU=jf,OU=jf,OU=pk,OU=User,DC=soton,DC=ac,DC=uk)".format(cluster)
      conn.search("dc=soton,dc=ac,dc=uk", search_filter, attributes=["cn"])
      current_users[cluster] = [entry.cn.value for entry in conn.entries]
    return current_users    
