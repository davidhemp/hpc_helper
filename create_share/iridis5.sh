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


echo "Creating share ${sharePath}/${shareName} with access given to: ${userArray[*]}"


## Create share
mkdir ${sharePath}/${shareName}
chmod 700 ${sharePath}/${shareName}
cd ${sharePath}/${shareName}


## Scratch ACL
cat << EOF > scratch.acl
#NFSv4 ACL
#owner:${OWNER}
#group:${GROUP}
special:owner@:rwxc:allow
 (X)READ/LIST (X)WRITE/CREATE (X)APPEND/MKDIR (X)SYNCHRONIZE (X)READ_ACL  (X)READ_ATTR  (X)READ_NAMED
 (-)DELETE    (X)DELETE_CHILD (X)CHOWN        (X)EXEC/SEARCH (X)WRITE_ACL (X)WRITE_ATTR (X)WRITE_NAMED

special:group@:----:allow
 (-)READ/LIST (-)WRITE/CREATE (-)APPEND/MKDIR (X)SYNCHRONIZE (X)READ_ACL  (X)READ_ATTR  (X)READ_NAMED
 (-)DELETE    (-)DELETE_CHILD (-)CHOWN        (-)EXEC/SEARCH (-)WRITE_ACL (-)WRITE_ATTR (-)WRITE_NAMED

special:everyone@:----:allow
 (-)READ/LIST (-)WRITE/CREATE (-)APPEND/MKDIR (X)SYNCHRONIZE (X)READ_ACL  (X)READ_ATTR  (X)READ_NAMED
 (-)DELETE    (-)DELETE_CHILD (-)CHOWN        (-)EXEC/SEARCH (-)WRITE_ACL (-)WRITE_ATTR (-)WRITE_NAMED
EOF

for user in ${userArray[*]}; do
cat << EOF >> scratch.acl
user:${user}:--x-:allow
 (-)READ/LIST (-)WRITE/CREATE (-)APPEND/MKDIR (X)SYNCHRONIZE (X)READ_ACL  (X)READ_ATTR  (X)READ_NAMED
 (-)DELETE    (-)DELETE_CHILD (-)CHOWN        (X)EXEC/SEARCH (-)WRITE_ACL (-)WRITE_ATTR (-)WRITE_NAMED
EOF
done

## Share ACLs
cat << EOF > share_dir.acl
#NFSv4 ACL
#owner:${OWNER}
#group:${GROUP}
special:owner@:rwxc:allow:DirInherit
 (X)READ/LIST (X)WRITE/CREATE (X)APPEND/MKDIR (X)SYNCHRONIZE (X)READ_ACL  (X)READ_ATTR  (X)READ_NAMED
 (X)DELETE    (X)DELETE_CHILD (X)CHOWN        (X)EXEC/SEARCH (X)WRITE_ACL (X)WRITE_ATTR (X)WRITE_NAMED

special:owner@:rw-c:allow:FileInherit
(X)READ/LIST (X)WRITE/CREATE (X)APPEND/MKDIR (X)SYNCHRONIZE (X)READ_ACL (X)READ_ATTR (X)READ_NAMED
(X)DELETE (X)DELETE_CHILD (X)CHOWN (-)EXEC/SEARCH (X)WRITE_ACL (X)WRITE_ATTR (X)WRITE_NAMED

special:group@:----:allow
 (-)READ/LIST (-)WRITE/CREATE (-)APPEND/MKDIR (X)SYNCHRONIZE (X)READ_ACL  (X)READ_ATTR  (X)READ_NAMED
 (-)DELETE    (-)DELETE_CHILD (-)CHOWN        (-)EXEC/SEARCH (-)WRITE_ACL (-)WRITE_ATTR (-)WRITE_NAMED

special:everyone@:----:allow
 (-)READ/LIST (-)WRITE/CREATE (-)APPEND/MKDIR (X)SYNCHRONIZE (X)READ_ACL  (X)READ_ATTR  (X)READ_NAMED
 (-)DELETE    (-)DELETE_CHILD (-)CHOWN        (-)EXEC/SEARCH (-)WRITE_ACL (-)WRITE_ATTR (-)WRITE_NAMED
EOF

for user in ${userArray[*]}; do
cat << EOF >> share_dir.acl
user:${user}:rwxc:allow:DirInherit
 (X)READ/LIST (X)WRITE/CREATE (X)APPEND/MKDIR (X)SYNCHRONIZE (X)READ_ACL  (X)READ_ATTR  (X)READ_NAMED
 (X)DELETE    (X)DELETE_CHILD (X)CHOWN        (X)EXEC/SEARCH (X)WRITE_ACL (X)WRITE_ATTR (X)WRITE_NAMED
user:${user}:rw-c:allow:FileInherit
 (X)READ/LIST (X)WRITE/CREATE (X)APPEND/MKDIR (X)SYNCHRONIZE (X)READ_ACL  (X)READ_ATTR  (X)READ_NAMED
 (X)DELETE    (X)DELETE_CHILD (X)CHOWN        (-)EXEC/SEARCH (X)WRITE_ACL (X)WRITE_ATTR (X)WRITE_NAMED
EOF
done

cat << EOF > share.acl
#NFSv4 ACL
#owner:${OWNER}
#group:${GROUP}
special:owner@:rw-c:allow
 (X)READ/LIST (X)WRITE/CREATE (X)APPEND/MKDIR (X)SYNCHRONIZE (X)READ_ACL  (X)READ_ATTR  (X)READ_NAMED
 (X)DELETE    (X)DELETE_CHILD (X)CHOWN        (-)EXEC/SEARCH (X)WRITE_ACL (X)WRITE_ATTR (X)WRITE_NAMED

special:group@:----:allow
 (-)READ/LIST (-)WRITE/CREATE (-)APPEND/MKDIR (X)SYNCHRONIZE (X)READ_ACL  (X)READ_ATTR  (X)READ_NAMED
 (-)DELETE    (-)DELETE_CHILD (-)CHOWN        (-)EXEC/SEARCH (-)WRITE_ACL (-)WRITE_ATTR (-)WRITE_NAMED

special:everyone@:----:allow
 (-)READ/LIST (-)WRITE/CREATE (-)APPEND/MKDIR (X)SYNCHRONIZE (X)READ_ACL  (X)READ_ATTR  (X)READ_NAMED
 (-)DELETE    (-)DELETE_CHILD (-)CHOWN        (-)EXEC/SEARCH (-)WRITE_ACL (-)WRITE_ATTR (-)WRITE_NAMED
EOF

for user in ${userArray[*]}; do
cat << EOF >> share.acl
user:${user}:rw-c-:allow
 (X)READ/LIST (X)WRITE/CREATE (X)APPEND/MKDIR (X)SYNCHRONIZE (X)READ_ACL  (X)READ_ATTR  (X)READ_NAMED
 (X)DELETE    (X)DELETE_CHILD (X)CHOWN        (-)EXEC/SEARCH (X)WRITE_ACL (X)WRITE_ATTR (X)WRITE_NAMED
EOF
done



## Create update ACL script
cat << EOF > update_acl.sh
#!/bin/bash
SHARE_DIRECTORY=${sharePath}/${shareName}
if [ \$(whoami) == "${OWNER}" ] ; then
  mmputacl -i \${SHARE_DIRECTORY}/scratch.acl ${sharePath}/
  mmputacl -i \${SHARE_DIRECTORY}/share_dir.acl \${SHARE_DIRECTORY}
  chmod 644 \${SHARE_DIRECTORY}/share_dir.acl \${SHARE_DIRECTORY}/scratch.acl
fi
find \${SHARE_DIRECTORY} -type d -exec mmputacl -i \${SHARE_DIRECTORY}/share_dir.acl {} \;
find \${SHARE_DIRECTORY} ! -name '*.acl' ! -perm /u=x,g=x,o=x -type f -exec mmputacl -i \${SHARE_DIRECTORY}/share.acl {} \;
#find \${SHARE_DIRECTORY} ! -name '*.acl' ! -name 'update_acl.sh' -perm /u=x,g=x,o=x -type f -exec mmputacl -i \${SHARE_DIRECTORY}/share_x.acl {} \;
EOF
chmod 755 update_acl.sh
./update_acl.sh
