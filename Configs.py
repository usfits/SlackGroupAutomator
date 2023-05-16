# CONNECTION_CONFIGS - configs for connecting to the database and to slack

SLACK_SCIM_TOKEN = ""
DATABASE_HOSTNAME = "localhost"
DATABASE_PORT = "5432"
DATABASE_NAME = "usfmobile"
DATABASE_USERNAME = "postgres"
DATABASE_PASSWORD = "admin"


# SETTINGS - these are things we can configure to change our interaction with the slack api

CREATE_NEW_GROUPS = False # if true, will create new group if group does not exist, if false, will not create new group and will return an error if group does not exist
CREATE_NEW_USERS = False # if true, will create new user if user does not exist, if false, will not create new user and will return an error if user does not exist

# NEW_GROUP_SETTINGS - we can standardize group names and create them automatically if they don't exist
# eg. if we want to create a group for each year and major, we can set the group name to be the YEAR_MAJOR ie. 2021_COMPSCI_UNDERGRAD
GROUP_NAME_FORMAT = f"{{YEAR}}_{{MAJOR}}_UNDERGRAD_TEST" # this is the format of the group name, we can use the following keywords: YEAR, MAJOR, ROLE, and UNDERGRAD/GRAD

ALL_GROUPS = ["SkyteamTest"]

# MAPPINGS: mappings from information we get from db to slack groups

ROLE_TO_GROUP = {}
ROLE_TO_GROUP["STU"] = ["Students_TEST", "SkyteamTest_TEST1", "TestTest"]
ROLE_TO_GROUP["STUEMP"] = ["Students_TEST", "Employees_TEST"]
ROLE_TO_GROUP["FAC"] = ["Faculty_TEST"]
ROLE_TO_GROUP["EMP"] = ["Employees_TEST"]

MAJOR_TO_GROUP = {}
MAJOR_TO_GROUP["COMPSCI"] = ["usfcs", "mscs"]
MAJOR_TO_GROUP["ARTS"] = ["C01JZQZQZQZ"]
MAJOR_TO_GROUP["ECON"] = ["C01JZQZQZQZ"]
MAJOR_TO_GROUP["MBBS"] = ["C01JZQZQZQZ"]

YEAR_TO_GROUP = {}
YEAR_TO_GROUP["2019"] = ["C01JZQZQZQZ"]
YEAR_TO_GROUP["2020"] = ["C01JZQZQZQZ"]
YEAR_TO_GROUP["2021"] = ["C01JZQZQZQZ"]
YEAR_TO_GROUP["2022"] = ["C01JZQZQZQZ"]
YEAR_TO_GROUP["2023"] = ["2023Students_TEST"]


