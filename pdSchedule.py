#!/usr/bin/env python3

import requests
import keyring
import datetime
import getpass

# get some secrets - you should have items in your login keychain
# that match the names here. The pd api key needs to start with "Token token=".
# The Slack token needs to start with "Bearer xoxp-"
pd_api_key = keyring.get_password("pd_api_key", getpass.getuser())
slack_api_key = keyring.get_password("slack_api_key", getpass.getuser())

# set some constants
schedule = "PBVU1PI" # the schedule to check in PD
help_group = "SPFRQHDS8" # the slack group to add users to
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)

# get all the PD users on the final schedule
# get the big schedule from PD
print(">>Getting the schedule from Pagerduty")
r = requests.get("https://api.pagerduty.com/schedules/" + schedule + "?time_zone=UTC&since=" + today.strftime("%Y-%m-%d") + "&until=" + tomorrow.strftime("%Y-%m-%d"), headers={"Authorization": pd_api_key})

# we only want the final schedule
# print(r.text)
pd_schedule = r.json()['schedule']['final_schedule']['rendered_schedule_entries']
# there might be multiple users?
user_group = []
for i in pd_schedule:
    user = i['user']
    user_group.append(user['id'])

# de-duplicate the list of user IDs
user_group = list(set(user_group))
print(">>Turning UserIDs into email addresses")

# get email addresses from user IDs
emails = []
for user_id in user_group:
    r = requests.get("https://api.pagerduty.com/users/" + user_id, headers={"Authorization": pd_api_key})
    pd_user = r.json()['user']
    emails.append(pd_user['email'])

# let's de-dupe that too
emails = list(set(emails))

# let's get a sanity check from a human
print("About to set the group membership to " + ', '.join(emails))
print("Enter to continue, ctrl-c to abort.")
input()

# now we gotta get the Slack user ID from the email

# make some lists for slack users
found_users = set()
userIDs = []

# Slack is special, so we need to pull all users and then filter for the ones we want
r = requests.get("https://slack.com/api/users.list?pretty=1", headers={'Authorization': slack_api_key})
for i in r.json()['members']:
    if i['profile'].get('email') in emails:
        userIDs.append(i['id'])
        foo = i['profile'].get('email')
        found_users.add(foo.split("@")[0])
        print(foo.split("@")[0] + " is user id " + i['id'])
# userIDs list now contains all the slack IDs of the people who should be in the group today
# we need to turn this into a comma-separated string to feed to slack
all_users = ', '.join(userIDs)
# print(all_users)

# let's update that usergroup!
r = requests.post("https://slack.com/api/usergroups.users.update?usergroup=" + help_group + "&users=" + all_users, headers={'Authorization': slack_api_key})
print(r.text)





