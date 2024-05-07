#!/bin/bash

#Fill in the following
#SOMEF Configuration
# Set the Github Token
token=""
#
#SOCA Configuration
#database Host URL
host=""
#database Bucket
bucket=""
#database Organisation
org=""
#database Token
databaseToken="\n"
#######################
echo -e "${token}\n\n\n\n\n" | somef configure
#
echo "${databaseToken}"
socaCnf="${host}\n${bucket}\n${org}\n${databaseToken}\n"
echo -e "${socaCnf}" | soca configure