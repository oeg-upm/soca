#!/bin/bash

#Fill in the following
#SOMEF Configuration
# Set the Github Token
token=""
#
#SOCA Configuration
#database Host URL
host="http://influx:8086"
#database Bucket
bucket="my-bucket"
#database Organisation
org="org_name"
#database Token
databaseToken="wU0f32FuDEbEUXiKs2rKA-vlifTbO02hLB1v49hvwXWyVYLyPzyyBoBX8AT5LXuGRjZQcHn5ukp6GXnEkOriNA=="
#######################
echo -e "${token}\n\n\n\n" | somef configure
#
if [ -z "$databaseToken" ]; then
  databaseToken="\n"
fi
echo "${databaseToken}"
socaCnf="${host}\n${bucket}\n${org}\n${databaseToken}\n"
echo -e "${socaCnf}" | soca configure



