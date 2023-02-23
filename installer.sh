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
databaseToken=""
#######################
echo -e "${token}\n\n\n\n" | somef configure
#
if [ -z "$databaseToken" ]; then
  databaseToken="\n"
fi
echo "${databaseToken}"
socaCnf="${host}\n${bucket}\n${org}\n${databaseToken}\n"
echo -e "${socaCnf}" | soca configure



