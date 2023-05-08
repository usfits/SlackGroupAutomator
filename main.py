
import Constants
import Database
import SlackHandler

# dbHandler = Database.DBHandler(hostname=Constants.DATABASE_HOSTNAME, port=Constants.DATABASE_PORT, databaseName=Constants.DATABASE_NAME, databaseUser=Constants.DATABASE_USERNAME, databasePassword=Constants.DATABASE_PASSWORD)  

# columns = ["name", "email", "role", "major"]
# query = Database.DBHandler.contructQuery(queryType="SELECT", columns=columns, tableName="users")

# resultList = dbHandler.executeQuery(query=query, columns=columns)

# for row in resultList:
#     print(row)

slackHandler = SlackHandler.SlackHandler(scimToken=Constants.SLACK_SCIM_TOKEN)
# resp = slackHandler.searchUsers(startIndex=1, count=10)
resp = slackHandler.searchUsers(startIndex=1, count=10, filter="userName Eq 'gakulkarni' ")
print(resp)