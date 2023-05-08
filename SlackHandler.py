from slack_sdk import WebClient
from slack_sdk.scim import SCIMClient, Group
from slack_sdk.scim.v1.user import User, UserName, UserEmail
import Configs

# TODO - use user and group id in the populateUsers and populateGroups functions

# https://slack.dev/python-slack-sdk/scim/index.html
class SlackHandler:
    def __init__(self, scimToken: str) -> None:
        client = SCIMClient(token=Configs.SLACK_SCIM_TOKEN)
        self.client = client
        self.userInformation = {}
        self.groupInformation = {}

        self.populateUsers()
        self.populateGroups()

    
    def populateUsers(self) -> None:
        response = self.client.search_users(
            start_index=1,
            count=1000 ,
            # filter="userName Eq 'gskalele' "
        )

        # print(response.body)
        for resource in response.body['Resources']:
            userId = resource['id']
            userEmail = resource['emails'][0]['value']
            userGroups = resource['groups']
            userName = resource['userName']

            self.userInformation[userEmail] = {
                "slackId": userId,
                "userName": userName,
                "groupSet": set(),
            }

            for group in userGroups:
                # self.userInformation[userEmail]["groupList"].add(group)
                self.userInformation[userEmail]["groupSet"].add((group['value'], group['display']))
        
        # print(self.userInformation)
        return

    def populateGroups(self) -> None:
        response = self.client.search_groups(
            start_index=1,
            count=10,
        )

        for resource in response.body['Resources']:
            groupId = resource['id']
            groupName = resource['displayName']
            groupMembers = resource['members']

            self.groupInformation[groupName] = {
                "groupId": groupId,
                "memberSet": set(),
            }

            for member in groupMembers:
                self.groupInformation[groupName]["memberSet"].add((member['value'], member['display']))
        
        # for key, value in self.groupInformation.items():
        #     print(key + ' ---> ' + str(value))
        return

    def updateGroups(self, databaseResults: str, createNewGroups: bool, mappings: dict) -> None:
        roleToGroupMapping = mappings["ROLE_TO_GROUP"]
        groupSet = set()
        groupsToCreate = set()

        for _, value in roleToGroupMapping.items():
            for val in value:
                groupSet.add(val)
        
        for groupName in groupSet:
            if groupName not in self.groupInformation.keys():
                groupsToCreate.add(groupName)

        if len(groupsToCreate) > 0:
            self.createGroups(groupsToCreate=groupsToCreate)

        # print("printing")
        # print(self.userInformation)

        updatedGroupMembers = {}
        for row in databaseResults:
            i = self.userInformation[row["email"]]["slackId"]
            print(f"user email is {row['email']} and information is in next line userId is {i}")

            userRole = row["role"]

            userShouldBeInGroups = set(roleToGroupMapping[userRole])
            print(f"user should be in groups: {userShouldBeInGroups}")

            userIsInGroups = set([group[1] for group in self.userInformation[row["email"]]["groupSet"]])
            print(f"user is in groups: {userIsInGroups}")

            addUserToGroups = userShouldBeInGroups - userIsInGroups
            print(f"add user to groups: {addUserToGroups}")
            print()
            userSlackId = self.userInformation[row["email"]]["slackId"]

            for groups in addUserToGroups:
                groupId = self.groupInformation[groups]["groupId"]
                if groupId not in updatedGroupMembers:
                    updatedGroupMembers[groupId] = {}
                    updatedGroupMembers[groupId]["name"] = groups
                    updatedGroupMembers[groupId]["members"] = []
                
                updatedGroupMembers[groupId]["members"].append({'value': userSlackId, 'operation': 'add'})
        
        # print(updatedGroupMembers)

        for groupId, val in updatedGroupMembers.items():
            print(groupId + " ---> " + str(val["members"]) + " --> " + val["name"])
            groupToUpdate = Group(id=groupId, display_name=val['name'], members=val["members"])
            response = self.client.update_group(groupToUpdate)
            print("patched group")
            print(response.body)
            print("\n\n\n")

        

        return

    def searchUsers(self, startIndex: int, count: int, filter: str = "") -> list:
        # example of a filter -> filter="userName Eq 'gakulkarni' "
        response = self.client.search_users(
            start_index=startIndex,
            count=count,
            filter=filter,
        )
        return response.body
    
    def getGroups(self, startIndex: int, count: int) -> Group:
        groups = self.client.search_groups(
            start_index=1,
            count=10,
        )

        print(groups.body)
        return groups.body


    def createGroups(self, groupsToCreate: set) -> None:
        for groupName in groupsToCreate:
            group = Group(display_name=groupName, members=[])
            response = self.client.create_group(group)
            print(response)
        return
    
    def createGroup(self, groupName: str, members: list) -> Group:
        newGroup = Group(display_name=groupName)
        response = self.client.create_group(newGroup)
        return response.body

# newGroup = Group(display_name="SkyteamTest", members=[{'value': 'U04GB9TH6KW', 'display': 'Shubham Pareek'}, {'value': 'U04F2BQE05D', 'display': 'David Hyman'}, ])
# response = client.create_group(newGroup)

# print(response.body)
# msgBody = {
#     "schemas": [
#         "urn:scim:schemas:core:1.0"
#     ],
#     "members": [
#         {
#             "value": "userId",
#             "operation": "delete"
#         },
#         {
#             # add is done by default
#             "value": "U333CCC333"
#         }
#     ]
# }


# client.create_group(id="groupId", )

'''
check which all groups this user should be in
check which all groups this user is in
if user is not in a group, add user to that group
'''