#!/bin/bash

#SOMEF Configuration
# Set the Github Token
token="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"
######################
#SOCA Configuration
#Fill in the following
#database Host URL
host=""
#database Bucket
bucket=""
#database Token
databaseToken="G9tlsRl1J-dYeOYp5OkWGNOSipEmbeN3gyp0wBbxDp6KRSZ-1foOkdTbhj8rkhN7Onj7CV105OYAQqAvr4C8-w=="


#######################
if [ -z "$host" ]; then
  host="\n"
fi

if [ -z "$bucket" ]; then
  bucket="\n"
fi

if [ -z "$databaseToken" ]; then
  databaseToken="\n\n"
fi
###
#SOMEF command
echo -e "${token}\n\n\n\n" | somef configure
###
#SOCA command
echo "${databaseToken}"
socaCnf="${host}${bucket}${databaseToken}"
echo -e "${socaCnf}\n\n" | soca configure



