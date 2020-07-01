#!/bin/bash
if [[ "$#" -ne 1 ]] ; then
   echo "Usage: Give a username to search the database for"
   exit 1;
fi
DBusername=$(sed -n -e 's/^user = //p' database_key.py | tr -d '"')
DBpassword=$(sed -n -e 's/^password = //p' database_key.py | tr -d '"')
echo $DBusername
Query="select username,first_name,surname,pi_account,pi_name,pi_email,appl_date from IridisUsers.applicationsdev where username='${1}';"
mysql -h mysql431.soton.ac.uk -P 3306 -u ${DBusername} -p${DBpassword} -D IridisUsers -e "$Query"
