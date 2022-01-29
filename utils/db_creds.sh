#! /bin/sh

echo "Enter db user name:"
read user_name

stty -echo
echo "Password:"
read user_passwd
#read -s -p "Password:" user_passwd
stty echo

export OO_DB_USER="$user_name"
export OO_DB_PWD="$user_passwd"