#!/bin/bash
 
HOSTNAME="127.0.0.1"
PORT="3306"
USERNAME="root"
PASSWORD="12345678"
 
	                                          
DBNAME="comp3900_db"                                     \
#TABLENAME="test_table_name"
 
MYSQL_CMD="mysql -h ${HOSTNAME}  -P ${PORT}  -u ${USERNAME} -p"
echo ${MYSQL_CMD}
 
echo "drop database ${DBNAME}"
create_db_sql="drop database IF EXISTS ${DBNAME}"
echo ${create_db_sql}  | ${MYSQL_CMD}
if [ $? -ne 0 ]
then
 echo "drop databases ${DBNAME} failed ..."
 exit 1
fi
 
echo "create database ${DBNAME}"
create_db_sql="create database IF NOT EXISTS ${DBNAME} DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci"
echo ${create_db_sql}  | ${MYSQL_CMD}
if [ $? -ne 0 ]
then
 echo "create databases ${DBNAME} failed ..."
 exit 1
fi
 
# echo "create user ${DBNAME}"
# create_db_sql="grant all privileges on ${DBNAME}.* to ${DBNAME}@'%'  identified by 'yourpassword'"
# echo ${create_db_sql}  | ${MYSQL_CMD}                      \
# if [ $? -ne 0 ]
# then
#  echo "create user ${DBNAME} failed ..."
#  exit 1
# fi
