users=`ps axo user | grep -v "root\|nobody\|ntp\|rpc\|dbus\|rpcuser\|USER\|rtkit\|haldaemon\|dwh1d17\|djb1\|icw\|ev1r09"|uniq`
for user in $users; do pkill -u $user; done


#processes=`ps axo pid | grep -v "root\|nobody\|ntp\|rpc\|dbus\|rpcuser\|USER\|rtkit\|haldaemon\|dwh1d17\|djb1\|icw\|ev1r09"|uniq`
#for process in $processes; do kill $process; done
