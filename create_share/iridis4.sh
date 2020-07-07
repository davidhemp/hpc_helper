#!/bin/bash
OWNER=$(whoami)
GROUP=$(groups | cut -d" " -f1)
sharePath=/scratch/${OWNER}

echo "This script will create a shared directory in your scratch directory: ${sharePath}"
read -p "What would you like the share to be called? " shareName

echo "Please give the the usernames that require access. Press enter/return after each. Enter a blank line when done."
i=1
userArray=()
while read -p "User ${i}: " user; do
    [[ ${user} ]] || break
    rtn=`id ${user}` > /dev/null
    if [ $? -ne 0 ] ; then
        echo "Not a valid username"
    else
        userArray+=("${user}")
        i=$(( $i + 1 ))
    fi
done

userArray+=("${OWNER}")
uniqArray=`echo ${userArray[@]} | tr ' ' '\n' |sort -u | tr '\n' ' '`

echo "Creating share ${sharePath}/${shareName} with access given to: ${uniqArray[*]}"


## Create share
mkdir ${sharePath}/${shareName}
chmod 700 ${sharePath}/${shareName}
cd ${sharePath}/${shareName}


## Scratch ACL
cat << EOF > scratch.acl
#owner:${OWNER}
#group:${GROUP}
user::rwxc
group::----
other::----
mask::rwxc
EOF

for user in ${uniqArray[*]}; do
    echo "user:${user}:--x-" >> scratch.acl
done

## Share ACLs
cat << EOF > share_x.acl
#owner:${OWNER}
#group:${GROUP}
user::rwxc
group::----
other::----
mask::rwxc
user:${OWNER}:rwxc
EOF

for user in ${uniqArray[*]}; do
    echo "user:${user}:rwxc" >> share_x.acl
done

cat << EOF > share.acl
#owner:${OWNER}
#group:${GROUP}
user::rw-c
group::----
other::----
mask::rw-c
user:${OWNER}:rw-c
EOF

for user in ${uniqArray[*]}; do
    echo "user:${user}:rw-c" >> share.acl
done

## Create update ACL script
cat << EOF > update_acl.sh
#!/bin/bash
SHARE_DIRECTORY=${sharePath}/${shareName}
if [ \$(whoami) == "${OWNER}" ] ; then
  mmputacl -i \${SHARE_DIRECTORY}/scratch.acl ${sharePath}/
  mmputacl -i \${SHARE_DIRECTORY}/share_x.acl \${SHARE_DIRECTORY}
  mmputacl -d -i \${SHARE_DIRECTORY}/share_x.acl \${SHARE_DIRECTORY}
  chmod 644 \${SHARE_DIRECTORY}/share_x.acl \${SHARE_DIRECTORY}/share.acl \${SHARE_DIRECTORY}/scratch.acl
fi
find \${SHARE_DIRECTORY} -type d -exec mmputacl -d -i \${SHARE_DIRECTORY}/share_x.acl {} \;
find \${SHARE_DIRECTORY} ! -name '*.acl' ! -perm /u=x,g=x,o=x -type f -exec mmputacl -i \${SHARE_DIRECTORY}/share.acl {} \;
find \${SHARE_DIRECTORY} ! -name '*.acl' ! -name 'update_acl.sh' -perm /u=x,g=x,o=x -type f -exec mmputacl -i \${SHARE_DIRECTORY}/share_x.acl {} \;
EOF
chmod 755 update_acl.sh
./update_acl.sh
