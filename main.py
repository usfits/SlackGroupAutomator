
import Configs
import Database
import SlackHandler

def main():
    dbHandler = Database.DBHandler(hostname=Configs.DATABASE_HOSTNAME, port=Configs.DATABASE_PORT, databaseName=Configs.DATABASE_NAME, databaseUser=Configs.DATABASE_USERNAME, databasePassword=Configs.DATABASE_PASSWORD)  
    slackHandler = SlackHandler.SlackHandler(scimToken=Configs.SLACK_SCIM_TOKEN)

    columns = ["name", "email", "role", "major", "year"]
    query = Database.DBHandler.contructQuery(queryType="SELECT", columns=columns, tableName="users")

    resultList = dbHandler.executeQuery(query=query, columns=columns)

    # for row in resultList:
    #     print(row)
    
    mappings = {
        "ROLE_TO_GROUP": Configs.ROLE_TO_GROUP,
    }
    slackHandler.updateGroups(databaseResults=resultList, createNewGroups=Configs.CREATE_NEW_GROUPS, mappings=mappings)

    
if __name__ == "__main__":
    main()
