#!/bin/bash -x

soca fetch -i oeg-upm --org -o oeg-upm_repos --not_archived  #modify -i ______ to organisation, add --user if its a user
soca extract -i oeg-upm_repos -o oeg-upm_metadata -i4p
soca portal -i oeg-upm_metadata
soca summary -i portal/cards_data.json -U
