#!/bin/bash -x

soca fetch -i Str3am786 --user -o oeg-upm_repos.csv --not_archived  #modify -i ______ to organisation, add --user if its a user
soca extract -i oeg-upm_repos.csv -o oeg-upm_metadata
soca portal -i oeg-upm_metadata
soca summary -i portal/cards_data.json -U
